import { afterEach, beforeEach, describe, expect, jest, test } from '@jest/globals';
import { fileURLToPath } from 'node:url';

globalThis.fetch = jest.fn();
process.env['INPUT_GITHUB-TOKEN'] = 'test-token';
process.env.INPUT_REPOSITORY = 'cumbucadev/actionando';
process.env['INPUT_PULL-REQUEST-NUMBER'] = '12';
process.env['INPUT_PULL-REQUEST-AUTHOR'] = 'alice';

const action = await import('../index.js');

const api = 'https://api.github.com';

function response(body, status = 200, statusText = 'OK') {
  return {
    ok: status >= 200 && status < 300,
    status,
    statusText,
    json: jest.fn().mockResolvedValue(body),
    text: jest.fn().mockResolvedValue(typeof body === 'string' ? body : JSON.stringify(body)),
  };
}

function requests(method, path) {
  return fetch.mock.calls.filter(([url, options]) =>
    url === `${api}${path}` && (options?.method ?? 'GET') === method,
  );
}

beforeEach(() => {
  fetch.mockReset();
  process.env['INPUT_GITHUB-TOKEN'] = 'test-token';
  process.env.INPUT_REPOSITORY = 'cumbucadev/actionando';
  process.env.INPUT_MODE = 'validate';
  process.env['INPUT_PULL-REQUEST-NUMBER'] = '12';
  process.env['INPUT_PULL-REQUEST-AUTHOR'] = 'alice';
  jest.spyOn(console, 'log').mockImplementation(() => {});
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('GitHub API helpers', () => {
  test('sends authenticated GitHub headers and JSON request bodies', async () => {
    fetch.mockResolvedValue(response({ id: 1 }));

    await expect(action.request('/repos/cumbucadev/actionando/issues/12/labels', {
      method: 'POST',
      body: { labels: ['Needs Issue'] },
    })).resolves.toEqual({ id: 1 });

    expect(fetch).toHaveBeenCalledWith(`${api}/repos/cumbucadev/actionando/issues/12/labels`, {
      method: 'POST',
      headers: {
        Accept: 'application/vnd.github+json',
        Authorization: 'Bearer test-token',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ labels: ['Needs Issue'] }),
    });
  });

  test('throws an informative error for failed API responses', async () => {
    fetch.mockResolvedValue(response('Not found', 404, 'Not Found'));

    await expect(action.request('/missing')).rejects.toMatchObject({
      message: 'GitHub API request failed (404 Not Found): Not found',
      status: 404,
    });
  });

  test('falls back to the initially loaded token when the input is empty', async () => {
    process.env['INPUT_GITHUB-TOKEN'] = '';
    fetch.mockResolvedValue(response({ id: 1 }));

    await action.request('/repos/cumbucadev/actionando/issues/12');

    expect(fetch.mock.calls[0][1].headers.Authorization).toBe('Bearer test-token');
  });

  test('omits authorization when no token is available', async () => {
    const token = process.env['INPUT_GITHUB-TOKEN'];
    delete process.env['INPUT_GITHUB-TOKEN'];

    try {
      const actionWithoutToken = await import('../index.js?request-without-token');
      fetch.mockResolvedValue(response({ id: 1 }));
      await actionWithoutToken.request('/repos/cumbucadev/actionando/issues/12');
      expect(fetch.mock.calls[0][1].headers).not.toHaveProperty('Authorization');
    } finally {
      process.env['INPUT_GITHUB-TOKEN'] = token;
    }
  });

  test('rethrows label-removal errors other than 404', async () => {
    fetch.mockResolvedValue(response('Server error', 500, 'Internal Server Error'));

    await expect(action.removeLabel(12, action.LABEL_NEEDS_ISSUE)).rejects.toMatchObject({
      status: 500,
    });
  });

  test('does not post a generated comment when its marker already exists', async () => {
    fetch.mockResolvedValue(response([{ id: 90, body: `Existing ${action.MARKERS.needsIssue}` }]));

    await action.ensureComment(12, action.COMMENTS.needsIssue, action.MARKERS.needsIssue);

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(requests('POST', '/repos/cumbucadev/actionando/issues/12/comments')).toHaveLength(0);
  });

  test('paginates until a page contains fewer than 100 results', async () => {
    fetch
      .mockResolvedValueOnce(response(Array.from({ length: 100 }, (_, index) => index)))
      .mockResolvedValueOnce(response([100]));

    const result = await action.paginate('/repos/cumbucadev/actionando/issues', undefined);

    expect(result).toHaveLength(101);
    expect(fetch.mock.calls.map(([url]) => url)).toEqual([
      `${api}/repos/cumbucadev/actionando/issues?per_page=100&page=1`,
      `${api}/repos/cumbucadev/actionando/issues?per_page=100&page=2`,
    ]);
  });

  test('surfaces GraphQL errors', async () => {
    fetch.mockResolvedValue(response({ errors: [{ message: 'Permission denied' }] }));

    await expect(action.graphql('query {}', {})).rejects.toThrow(
      'GitHub GraphQL request failed: Permission denied',
    );
  });
});

describe('validate mode', () => {
  test('labels and comments on a pull request without a linked issue', async () => {
    fetch
      .mockResolvedValueOnce(response({ data: { repository: { pullRequest: { closingIssuesReferences: { nodes: [] } } } } }))
      .mockResolvedValueOnce(response([]))
      .mockResolvedValueOnce(response([]))
      .mockResolvedValueOnce(response([]));

    await expect(action.main()).rejects.toThrow('PR #12 is not linked to an issue.');

    expect(requests('POST', '/repos/cumbucadev/actionando/issues/12/labels')).toHaveLength(1);
    expect(fetch.mock.calls[1][1].body).toBe(JSON.stringify({ labels: [action.LABEL_NEEDS_ISSUE] }));
    expect(requests('POST', '/repos/cumbucadev/actionando/issues/12/comments')).toHaveLength(1);
    expect(JSON.parse(fetch.mock.calls[3][1].body).body).toContain(action.MARKERS.needsIssue);
  });

  test('reports an unassigned linked issue and labels both issue and pull request', async () => {
    fetch
      .mockResolvedValueOnce(response({ data: { repository: { pullRequest: { closingIssuesReferences: { nodes: [{ number: 34 }] } } } } }))
      .mockResolvedValueOnce(response(undefined, 404, 'Not Found'))
      .mockResolvedValueOnce(response({ assignees: [] }))
      .mockResolvedValueOnce(response([]))
      .mockResolvedValueOnce(response([]))
      .mockResolvedValueOnce(response([]))
      .mockResolvedValueOnce(response([]))
      .mockResolvedValueOnce(response([]))
      .mockResolvedValueOnce(response([]));

    await expect(action.main()).rejects.toThrow('Issue #34 has no assignee.');

    expect(requests('POST', '/repos/cumbucadev/actionando/issues/12/labels')).toHaveLength(1);
    expect(requests('POST', '/repos/cumbucadev/actionando/issues/34/labels')).toHaveLength(1);
    expect(requests('POST', '/repos/cumbucadev/actionando/issues/34/comments')).toHaveLength(1);
    expect(requests('POST', '/repos/cumbucadev/actionando/issues/12/comments')).toHaveLength(1);
    expect(fetch.mock.calls[1][1].method).toBe('DELETE');
  });

  test('reports assignment to a different user, removes stale comments, and comments on both records', async () => {
    const commentReads = new Map();
    fetch.mockImplementation(async (url, options = {}) => {
      if (url === `${api}/graphql`) {
        return response({
          data: { repository: { pullRequest: { closingIssuesReferences: { nodes: [{ number: 34 }] } } } },
        });
      }
      if (url === `${api}/repos/cumbucadev/actionando/issues/34` && options.method === 'GET') {
        return response({ assignees: [{ login: 'bob' }] });
      }
      if (url.includes('/labels/')) return response(undefined, 404, 'Not Found');
      if (url.includes('/comments?') && (options.method ?? 'GET') === 'GET') {
        const reads = commentReads.get(url) ?? 0;
        commentReads.set(url, reads + 1);
        if (reads > 0) return response([]);
        const id = url.includes('/issues/34/') ? 1 : 2;
        return response([{ id, body: action.MARKERS.needsAssignment }]);
      }
      return response(undefined, 204, 'No Content');
    });

    await expect(action.main()).rejects.toThrow(
      'Issue #34 is not assigned to PR author.',
    );

    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/comments/1')).toHaveLength(1);
    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/comments/2')).toHaveLength(1);
    expect(requests('POST', '/repos/cumbucadev/actionando/issues/34/comments')).toHaveLength(1);
    expect(requests('POST', '/repos/cumbucadev/actionando/issues/12/comments')).toHaveLength(1);
  });

  test('clears generated labels and comments when the issue is assigned to the pull request author', async () => {
    fetch.mockImplementation(async (url, options = {}) => {
      if (url === `${api}/graphql`) {
        return response({
          data: { repository: { pullRequest: { closingIssuesReferences: { nodes: [{ number: 34 }] } } } },
        });
      }
      if (url === `${api}/repos/cumbucadev/actionando/issues/34` && options.method === 'GET') {
        return response({ assignees: [{ login: 'alice' }, { login: 'bob' }] });
      }
      if (url.includes('/labels/')) return response(undefined, 404, 'Not Found');
      if (url.includes('/comments?') && (options.method ?? 'GET') === 'GET') {
        return response([
          { id: 10, body: action.MARKERS.needsIssue },
          { id: 11, body: action.MARKERS.unassigned },
          { id: 12, body: action.MARKERS.otherAssignee },
          { id: 13, body: action.MARKERS.needsAssignment },
        ]);
      }
      return response(undefined, 204, 'No Content');
    });

    await expect(action.main()).resolves.toBeUndefined();

    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/12/labels/Needs%20Assignment')).toHaveLength(1);
    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/34/labels/Needs%20Assignment')).toHaveLength(1);
    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/comments/10')).toHaveLength(1);
    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/comments/11')).toHaveLength(2);
    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/comments/12')).toHaveLength(2);
    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/comments/13')).toHaveLength(2);
    expect(requests('POST', '/repos/cumbucadev/actionando/issues/12/comments')).toHaveLength(0);
  });
});

describe('cleanup mode', () => {
  test('removes generated comments and assignment labels from unlinked issues', async () => {
    const query = `repo:cumbucadev/actionando is:issue is:open label:"${action.LABEL_NEEDS_ASSIGNMENT}" -linked:pr`;
    fetch
      .mockResolvedValueOnce(response({ items: [{ number: 51 }] }))
      .mockResolvedValueOnce(response([{ id: 20, body: action.MARKERS.unassigned }]))
      .mockResolvedValueOnce(response(undefined, 204, 'No Content'))
      .mockResolvedValueOnce(response([{ id: 21, body: action.MARKERS.otherAssignee }]))
      .mockResolvedValueOnce(response(undefined, 204, 'No Content'))
      .mockResolvedValueOnce(response([{ id: 22, body: action.MARKERS.needsAssignment }]))
      .mockResolvedValueOnce(response(undefined, 204, 'No Content'))
      .mockResolvedValueOnce(response(undefined, 404, 'Not Found'));
    process.env.INPUT_MODE = 'cleanup';

    await expect(action.main()).resolves.toBeUndefined();

    expect(fetch.mock.calls[0][0]).toBe(`${api}/search/issues?q=${encodeURIComponent(query)}&per_page=100&page=1`);
    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/comments/20')).toHaveLength(1);
    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/comments/21')).toHaveLength(1);
    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/comments/22')).toHaveLength(1);
    expect(requests('DELETE', '/repos/cumbucadev/actionando/issues/51/labels/Needs%20Assignment')).toHaveLength(1);
  });
});

describe('rerun mode', () => {
  test('reruns the latest matching workflow for unique linked pull requests in numeric order', async () => {
    fetch
      .mockResolvedValueOnce(response([
        { event: 'cross-referenced', source: { issue: { number: 9, pull_request: {} } } },
        { event: 'cross-referenced', source: { issue: { number: 3, pull_request: {} } } },
        { event: 'cross-referenced', source: { issue: { number: 9, pull_request: {} } } },
        { event: 'mentioned', source: { issue: { number: 1, pull_request: {} } } },
      ]))
      .mockResolvedValueOnce(response({ workflows: [{ id: 77, name: 'Verify Assign and Link' }] }))
      .mockResolvedValueOnce(response({ head: { sha: 'sha-three' } }))
      .mockResolvedValueOnce(response({ workflow_runs: [] }))
      .mockResolvedValueOnce(response({ head: { sha: 'sha-nine' } }))
      .mockResolvedValueOnce(response({ workflow_runs: [
        { id: 1, event: 'pull_request_target', created_at: '2025-01-01T00:00:00Z' },
        { id: 2, event: 'pull_request_target', created_at: '2025-02-01T00:00:00Z' },
        { id: 3, event: 'push', created_at: '2025-03-01T00:00:00Z' },
      ] }))
      .mockResolvedValueOnce(response(undefined, 204, 'No Content'))
    process.env.INPUT_MODE = 'rerun';
    process.env['INPUT_ISSUE-NUMBER'] = '34';

    await expect(action.main()).resolves.toBeUndefined();

    expect(fetch.mock.calls[2][0]).toBe(`${api}/repos/cumbucadev/actionando/pulls/3`);
    expect(fetch.mock.calls[3][0]).toContain('head_sha=sha-three');
    expect(fetch.mock.calls[4][0]).toBe(`${api}/repos/cumbucadev/actionando/pulls/9`);
    expect(fetch.mock.calls[5][0]).toContain('head_sha=sha-nine');
    expect(requests('POST', '/repos/cumbucadev/actionando/actions/runs/2/rerun')).toHaveLength(1);
  });

  test('returns without looking up workflows when no pull requests are linked', async () => {
    fetch.mockResolvedValue(response([]));
    process.env.INPUT_MODE = 'rerun';
    process.env['INPUT_ISSUE-NUMBER'] = '34';

    await expect(action.main()).resolves.toBeUndefined();

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch.mock.calls[0][0]).toContain('/issues/34/timeline');
  });

  test('fails clearly when the expected workflow is missing', async () => {
    fetch
      .mockResolvedValueOnce(response([
        { event: 'cross-referenced', source: { issue: { number: 3, pull_request: {} } } },
      ]))
      .mockResolvedValueOnce(response({ workflows: [] }));
    process.env.INPUT_MODE = 'rerun';
    process.env['INPUT_ISSUE-NUMBER'] = '34';

    await expect(action.main()).rejects.toThrow("Workflow 'Verify Assign and Link' not found.");
  });
});

describe('input validation', () => {
  test('requires a GitHub token', async () => {
    const token = process.env['INPUT_GITHUB-TOKEN'];
    const repository = process.env.INPUT_REPOSITORY;
    delete process.env['INPUT_GITHUB-TOKEN'];
    process.env.INPUT_REPOSITORY = '';

    try {
      const actionWithoutToken = await import('../index.js?missing-token');
      await expect(actionWithoutToken.main()).rejects.toThrow(
        'The github-token input is required.',
      );
      expect(fetch).not.toHaveBeenCalled();
    } finally {
      process.env['INPUT_GITHUB-TOKEN'] = token;
      process.env.INPUT_REPOSITORY = repository;
    }
  });

  test('requires the repository to use owner/name format', async () => {
    const repository = process.env.INPUT_REPOSITORY;
    process.env.INPUT_REPOSITORY = 'invalid';

    try {
      const actionWithoutRepository = await import('../index.js?missing-repository');
      await expect(actionWithoutRepository.main()).rejects.toThrow(
        'The repository input must be in owner/name format.',
      );
      expect(fetch).not.toHaveBeenCalled();
    } finally {
      process.env.INPUT_REPOSITORY = repository;
    }
  });

  test('rejects unsupported modes', async () => {
    process.env.INPUT_MODE = 'unsupported';

    await expect(action.main()).rejects.toThrow('Unsupported mode: unsupported');
    expect(fetch).not.toHaveBeenCalled();
  });

  test('logs failures when the action is directly executed', async () => {
    const argv = process.argv[1];
    const exitCode = process.exitCode;
    const error = jest.spyOn(console, 'error').mockImplementation(() => {});
    process.argv[1] = fileURLToPath(new URL('../index.js', import.meta.url));
    process.env.INPUT_MODE = 'unsupported';

    try {
      await jest.isolateModulesAsync(async () => {
        await import('../index.js');
      });
      await new Promise((resolve) => setImmediate(resolve));

      expect(error).toHaveBeenCalledWith(
        expect.objectContaining({ message: 'Unsupported mode: unsupported' }),
      );
      expect(process.exitCode).toBe(1);
    } finally {
      process.argv[1] = argv;
      if (exitCode === undefined) process.exitCode = 0;
      else process.exitCode = exitCode;
    }
  });
});
