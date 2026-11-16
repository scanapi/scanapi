import { pathToFileURL } from 'node:url';
import { MARKERS, COMMENTS, LABEL_NEEDS_ISSUE, LABEL_NEEDS_ASSIGNMENT } from './marks-comments.js';
const API_URL = 'https://api.github.com';


const token = process.env['INPUT_GITHUB-TOKEN'];
const repository = process.env.INPUT_REPOSITORY;
const [owner, repo] = (repository || '').split('/');

async function request(path, { method = 'GET', body } = {}) {
  const authToken = process.env['INPUT_GITHUB-TOKEN'] || token;
  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers: {
      Accept: 'application/vnd.github+json',
      ...(authToken ? { Authorization: 'Bearer ' + authToken } : {}),
      'X-GitHub-Api-Version': '2022-11-28',
      ...(body === undefined ? {} : { 'Content-Type': 'application/json' }),
    },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }),
  });

  if (!response.ok) {
    const details = await response.text();
    const error = new Error(
      `GitHub API request failed (${response.status} ${response.statusText}): ${details}`,
    );
    error.status = response.status;
    throw error;
  }

  return response.status === 204 ? undefined : response.json();
}

async function paginate(path, resultKey) {
  const results = [];

  for (let page = 1; ; page += 1) {
    const separator = path.includes('?') ? '&' : '?';
    const response = await request(`${path}${separator}per_page=100&page=${page}`);
    const items = resultKey ? response[resultKey] : response;
    results.push(...items);
    if (items.length < 100) return results;
  }
}

async function graphql(query, variables) {
  const response = await request('/graphql', {
    method: 'POST',
    body: { query, variables },
  });

  if (response.errors?.length) {
    throw new Error(`GitHub GraphQL request failed: ${response.errors.map(({ message }) => message).join('; ')}`);
  }
  return response.data;
}

async function addLabel(number, label) {
  await request(`/repos/${owner}/${repo}/issues/${number}/labels`, {
    method: 'POST',
    body: { labels: [label] },
  });
}

async function removeLabel(number, label) {
  try {
    await request(`/repos/${owner}/${repo}/issues/${number}/labels/${encodeURIComponent(label)}`, {
      method: 'DELETE',
    });
  } catch (error) {
    if (error.status !== 404) throw error;
  }
}

async function comments(number) {
  return paginate(`/repos/${owner}/${repo}/issues/${number}/comments`);
}

async function ensureComment(number, body, marker) {
  const existingComments = await comments(number);
  if (existingComments.some((comment) => comment.body.includes(marker))) return;
  await request(`/repos/${owner}/${repo}/issues/${number}/comments`, {
    method: 'POST',
    body: { body },
  });
}

async function removeGeneratedComments(number, marker) {
  const existingComments = await comments(number);
  for (const comment of existingComments) {
    if (comment.body.includes(marker)) {
      await request(`/repos/${owner}/${repo}/issues/comments/${comment.id}`, {
        method: 'DELETE',
      });
    }
  }
}

async function linkedIssueNumber(pullRequestNumber) {
  const data = await graphql(
    `query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $number) {
          closingIssuesReferences(first: 1) {
            nodes { number }
          }
        }
      }
    }`,
    { owner, repo, number: Number(pullRequestNumber) },
  );
  return data.repository?.pullRequest?.closingIssuesReferences?.nodes?.[0]?.number;
}

async function validate() {
  const pullRequestNumber = process.env['INPUT_PULL-REQUEST-NUMBER'];
  const pullRequestAuthor = process.env['INPUT_PULL-REQUEST-AUTHOR'];
  console.log(`Validating PR #${pullRequestNumber}`);
  console.log(`PR author: ${pullRequestAuthor}`);

  const issueNumber = await linkedIssueNumber(pullRequestNumber);
  if (!issueNumber) {
    console.log(`PR #${pullRequestNumber} is not linked to an issue.`);
    await addLabel(pullRequestNumber, LABEL_NEEDS_ISSUE);
    await ensureComment(pullRequestNumber, COMMENTS.needsIssue, MARKERS.needsIssue);
    throw new Error(`PR #${pullRequestNumber} is not linked to an issue.`);
  }

  console.log(`PR #${pullRequestNumber} is linked to issue #${issueNumber}.`);
  await removeLabel(pullRequestNumber, LABEL_NEEDS_ISSUE);

  const issue = await request(`/repos/${owner}/${repo}/issues/${issueNumber}`);
  const assignees = issue.assignees.map(({ login }) => login);

  if (assignees.length === 0) {
    console.log(`Issue #${issueNumber} has no assignee.`);
    await addLabel(pullRequestNumber, LABEL_NEEDS_ASSIGNMENT);
    await addLabel(issueNumber, LABEL_NEEDS_ASSIGNMENT);
    await ensureComment(issueNumber, COMMENTS.unassigned, MARKERS.unassigned);
    await ensureComment(pullRequestNumber, COMMENTS.unassigned, MARKERS.unassigned);
    throw new Error(`Issue #${issueNumber} has no assignee.`);
  }

  if (!assignees.includes(pullRequestAuthor)) {
    console.log(`Issue #${issueNumber} is not assigned to PR author.`);
    console.log(`Assignees: ${assignees.join(', ')}`);
    console.log(`PR author: ${pullRequestAuthor}`);
    await addLabel(pullRequestNumber, LABEL_NEEDS_ASSIGNMENT);
    await addLabel(issueNumber, LABEL_NEEDS_ASSIGNMENT);
    await removeGeneratedComments(issueNumber, MARKERS.needsAssignment);
    await removeGeneratedComments(pullRequestNumber, MARKERS.needsAssignment);
    await ensureComment(issueNumber, COMMENTS.otherAssignee, MARKERS.otherAssignee);
    await ensureComment(pullRequestNumber, COMMENTS.otherAssignee, MARKERS.otherAssignee);
    throw new Error(`Issue #${issueNumber} is not assigned to PR author.`);
  }

  console.log(`Issue #${issueNumber} is correctly assigned to ${pullRequestAuthor}.`);
  await removeLabel(pullRequestNumber, LABEL_NEEDS_ASSIGNMENT);
  await removeLabel(issueNumber, LABEL_NEEDS_ASSIGNMENT);
  await removeGeneratedComments(pullRequestNumber, MARKERS.needsIssue);
  for (const marker of [MARKERS.unassigned, MARKERS.otherAssignee, MARKERS.needsAssignment]) {
    await removeGeneratedComments(issueNumber, marker);
    await removeGeneratedComments(pullRequestNumber, marker);
  }
  console.log('Validation passed.');
}

async function cleanupUnlinkedIssues() {
  const query = `repo:${repository} is:issue is:open label:"${LABEL_NEEDS_ASSIGNMENT}" -linked:pr`;
  const path = `/search/issues?q=${encodeURIComponent(query)}`;
  const issues = await paginate(path, 'items');

  for (const issue of issues) {
    console.log(`Removing generated comments from issue #${issue.number}`);
    for (const marker of [MARKERS.unassigned, MARKERS.otherAssignee, MARKERS.needsAssignment]) {
      await removeGeneratedComments(issue.number, marker);
    }
    await removeLabel(issue.number, LABEL_NEEDS_ASSIGNMENT);
  }
}

async function rerunLinkedPullRequests() {
  const issueNumber = process.env['INPUT_ISSUE-NUMBER'];
  console.log(`Issue #${issueNumber} changed.`);

  const timeline = await paginate(
    `/repos/${owner}/${repo}/issues/${issueNumber}/timeline`,
  );
  const pullRequestNumbers = [
    ...new Set(
      timeline
        .filter((event) => event.event === 'cross-referenced' && event.source?.issue?.pull_request)
        .map((event) => event.source.issue.number),
    ),
  ].sort((a, b) => a - b);

  if (pullRequestNumbers.length === 0) {
    console.log(`No pull request linked to issue #${issueNumber}.`);
    return;
  }
  console.log(`Linked PRs: ${pullRequestNumbers.map((number) => `#${number}`).join(', ')}`);

  const workflows = await paginate(`/repos/${owner}/${repo}/actions/workflows`, 'workflows');
  const workflow = workflows.find(({ name }) => name === 'Verify Assign and Link');
  if (!workflow) throw new Error("Workflow 'Verify Assign and Link' not found.");
  console.log(`Workflow ID: ${workflow.id}`);

  for (const pullRequestNumber of pullRequestNumbers) {
    console.log(`Processing PR #${pullRequestNumber}`);
    const pullRequest = await request(`/repos/${owner}/${repo}/pulls/${pullRequestNumber}`);
    console.log(`PR head SHA: ${pullRequest.head.sha}`);

    const runs = await paginate(
      `/repos/${owner}/${repo}/actions/workflows/${workflow.id}/runs?event=pull_request_target&head_sha=${pullRequest.head.sha}`,
      'workflow_runs',
    );
    const latestRun = runs
      .filter((run) => run.event === 'pull_request_target')
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))[0];

    if (!latestRun) {
      console.log(`No Verify Assign and Link run found for PR #${pullRequestNumber}.`);
      continue;
    }

    console.log(`Found run ${latestRun.id} for PR #${pullRequestNumber}.`);
    await request(`/repos/${owner}/${repo}/actions/runs/${latestRun.id}/rerun`, {
      method: 'POST',
    });
    console.log(`Rerun requested for PR #${pullRequestNumber}.`);
  }
}

export async function main() {
  if (!token) throw new Error('The github-token input is required.');
  if (!owner || !repo) throw new Error('The repository input must be in owner/name format.');

  switch (process.env.INPUT_MODE) {
    case 'validate':
      await validate();
      break;
    case 'cleanup':
      await cleanupUnlinkedIssues();
      break;
    case 'rerun':
      await rerunLinkedPullRequests();
      break;
    default:
      throw new Error(`Unsupported mode: ${process.env.INPUT_MODE}`);
  }
}

const isDirectExecution = process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;

if (isDirectExecution) {
  main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
}

export {
  request,
  paginate,
  graphql,
  addLabel,
  removeLabel,
  comments,
  ensureComment,
  removeGeneratedComments,
  linkedIssueNumber,
  validate,
  cleanupUnlinkedIssues,
  rerunLinkedPullRequests,
  LABEL_NEEDS_ISSUE,
  LABEL_NEEDS_ASSIGNMENT,
  MARKERS,
  COMMENTS,
};
