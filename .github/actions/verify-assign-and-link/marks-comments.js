const LABEL_NEEDS_ISSUE = 'Needs Issue';
const LABEL_NEEDS_ASSIGNMENT = 'Needs Assignment';

const MARKERS = {
  needsIssue: '<!-- verify-assign-and-link:Needs Issue -->',
  unassigned: '<!-- verify-assign-and-link:Needs Assignment:unassigned -->',
  otherAssignee: '<!-- verify-assign-and-link:Needs Assignment:other -->',
  needsAssignment: '<!-- verify-assign-and-link:Needs Assignment -->',
};

const COMMENTS = {
  needsIssue: `${MARKERS.needsIssue}

🇧🇷 **Português**

Esta PR não está vinculada a uma issue. Por favor, vincule a issue que esta PR pretende resolver antes de continuar. Siga o [Guia do Contribuidor](https://readthedocs.io) para aprender como vincular uma issue à sua PR. As PRs devem estar associadas a uma issue antes do início da implementação.

🇬🇧 **English**

This PR is not linked to an issue. Please link the issue this PR is intended to resolve before continuing. Please follow the [Contributor Guide](https://readthedocs.io) to learn how to link an issue to a PR. PRs should be associated with an issue before implementation starts.`,
  unassigned: `${MARKERS.unassigned}

🇧🇷 **Português**

Esta issue ainda não está atribuída a ninguém. Por favor, atribua a issue a você antes de abrir uma PR. Siga o [Guia do Contribuidor](https://readthedocs.io) para aprender como reivindicar uma issue. Isso ajuda a evitar que várias pessoas trabalhem na mesma issue ao mesmo tempo.

🇬🇧 **English**

This issue is not assigned to anyone yet. Please assign the issue to yourself before opening a PR. Please follow the [Contributor Guide](https://readthedocs.io) to learn how to claim an issue. This helps us avoid multiple people working on the same issue at the same time.`,
  otherAssignee: `${MARKERS.otherAssignee}

🇧🇷 **Português**

Esta issue está atualmente atribuída a outra pessoa. Por favor, coordene com o responsável antes de abrir uma PR para esta issue. Se você pretende trabalhar nela, certifique-se de que a issue esteja atribuída a você primeiro. Veja o [Guia do Contribuidor](https://readthedocs.io) para mais informações.

🇬🇧 **English**

This issue is currently assigned to someone else. Please coordinate with the assignee before opening a PR for this issue. If you intend to work on it, please make sure the issue is assigned to you first. See the [Contributor Guide](https://readthedocs.io) for more information.`,
};


export { LABEL_NEEDS_ISSUE, LABEL_NEEDS_ASSIGNMENT, MARKERS, COMMENTS };
