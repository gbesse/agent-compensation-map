const messages = {
  fr: {
    eyebrow: 'AGENTS · APRÈS L’APPEL, QUE S’EST-IL PASSÉ ?',
    title: 'Pas de réponse.\nPas forcément zéro effet.',
    lede: 'Deux tentatives ambiguës peuvent laisser zéro, un ou deux paiements. Un plan sûr dans le modèle doit observer avant de compenser, et reconnaître ce qu’il ne sait pas annuler.',
    uncertainty: 'Décrire l’incertitude',
    attempts: 'Tentatives au résultat inconnu',
    observe: 'La lecture des paiements est disponible',
    irreversible: 'Une notification a déjà été envoyée',
    depth: 'Profondeur maximale',
    plan: 'Chercher le plan conditionnel →',
    simulation:
      'Planification et rejeu synthétiques. Aucune compensation, lecture bancaire ou notification réelle n’est exécutée.',
    tree: 'Un arbre, pas un remboursement aveugle',
    worlds: 'mondes possibles',
    cost: 'coût maximal déclaré',
    verified: 'rejeu indépendant',
    replays: 'Chaque monde a son parcours',
    download: 'Exporter le plan et les preuves',
    limits:
      'Modèle fini fourni par l’utilisateur. Les actions futures et observations sont supposées déterministes et fiables dans ce modèle. Une limite de profondeur n’est pas une preuve d’impossibilité générale. MCP en lecture seule ; aucun moteur d’exécution distante ou garantie de résultat réel.',
    optimal: 'MINIMUM DANS LA BORNE',
    feasible: 'PLAN À REVOIR',
    review: 'REVUE HUMAINE NÉCESSAIRE',
    valid: 'valide',
    busy: 'Exploration des mondes possibles…',
    ready: 'Plan vérifié sur tous les mondes modélisés.',
    error: 'Entrée non valide ou serveur indisponible.',
    no_plan_within_depth_bound: 'Aucun plan trouvé dans cette borne de profondeur.',
    search_budget_exhausted: 'Budget de recherche épuisé ; aucun plan complet démontré.',
    unreachable_immutable_goal:
      'Un effet constaté ne peut être modifié par aucune compensation déclarée.',
    release_stock: 'Libérer la réservation',
    refund_one: 'Compenser un paiement',
    cancel_order: 'Annuler la commande simulée',
    read_charge_count: 'Observer le nombre de paiements',
    done: 'Objectif atteint dans le modèle',
    branch: 'Observation',
    charges: 'paiements initiaux',
    modelCost: 'coût',
  },
  en: {
    eyebrow: 'AGENTS · WHAT HAPPENED AFTER THE CALL?',
    title: 'No response.\nNot necessarily no effect.',
    lede: 'Two ambiguous attempts may leave zero, one or two payments. A model-safe plan observes before compensating and recognizes what it cannot undo.',
    uncertainty: 'Describe uncertainty',
    attempts: 'Attempts with unknown outcomes',
    observe: 'Payment readback is available',
    irreversible: 'A notification was already sent',
    depth: 'Maximum depth',
    plan: 'Find a contingent plan →',
    simulation:
      'Synthetic planning and replay. No real compensation, bank read or notification is executed.',
    tree: 'A tree, not a blind refund',
    worlds: 'possible worlds',
    cost: 'declared worst-case cost',
    verified: 'independent replay',
    replays: 'Each world has its path',
    download: 'Export plan and evidence',
    limits:
      'Finite user-supplied model. Future actions and observations are assumed deterministic and reliable within it. A depth limit does not prove general impossibility. Read-only MCP; no remote executor or real-world outcome guarantee.',
    optimal: 'MINIMUM WITHIN BOUND',
    feasible: 'PLAN FOR REVIEW',
    review: 'HUMAN REVIEW REQUIRED',
    valid: 'valid',
    busy: 'Exploring possible worlds…',
    ready: 'Plan checked in every modeled world.',
    error: 'Invalid input or server unavailable.',
    no_plan_within_depth_bound: 'No plan found within this depth bound.',
    search_budget_exhausted: 'Search budget exhausted; no complete plan established.',
    unreachable_immutable_goal:
      'An observed effect cannot be changed by any declared compensation.',
    release_stock: 'Release reservation',
    refund_one: 'Compensate one payment',
    cancel_order: 'Cancel simulated order',
    read_charge_count: 'Observe payment count',
    done: 'Model goal reached',
    branch: 'Observation',
    charges: 'initial payments',
    modelCost: 'cost',
  },
  es: {
    eyebrow: 'AGENTES · ¿QUÉ PASÓ DESPUÉS DE LA LLAMADA?',
    title: 'Sin respuesta.\nNo necesariamente sin efecto.',
    lede: 'Dos intentos ambiguos pueden dejar cero, uno o dos pagos. El plan seguro en el modelo observa antes de compensar y reconoce lo que no puede deshacer.',
    uncertainty: 'Describir incertidumbre',
    attempts: 'Intentos con resultado desconocido',
    observe: 'Se puede consultar el número de pagos',
    irreversible: 'Ya se envió una notificación',
    depth: 'Profundidad máxima',
    plan: 'Buscar plan condicional →',
    simulation:
      'Planificación y reproducción sintéticas. Sin compensaciones, consultas bancarias ni notificaciones reales.',
    tree: 'Un árbol, no un reembolso a ciegas',
    worlds: 'mundos posibles',
    cost: 'coste máximo declarado',
    verified: 'reproducción independiente',
    replays: 'Cada mundo tiene su recorrido',
    download: 'Exportar plan y pruebas',
    limits:
      'Modelo finito del usuario. Acciones y observaciones futuras se suponen deterministas y fiables dentro del modelo. El límite de profundidad no demuestra imposibilidad general. MCP de solo lectura; sin ejecutor remoto ni garantía de resultados reales.',
    optimal: 'MÍNIMO DENTRO DEL LÍMITE',
    feasible: 'PLAN PARA REVISAR',
    review: 'SE REQUIERE REVISIÓN HUMANA',
    valid: 'válido',
    busy: 'Explorando mundos posibles…',
    ready: 'Plan comprobado en todos los mundos modelados.',
    error: 'Entrada no válida o servidor no disponible.',
    no_plan_within_depth_bound: 'No se encontró plan dentro de esta profundidad.',
    search_budget_exhausted: 'Presupuesto agotado; no se estableció un plan completo.',
    unreachable_immutable_goal: 'Ninguna compensación declarada puede cambiar un efecto observado.',
    release_stock: 'Liberar reserva',
    refund_one: 'Compensar un pago',
    cancel_order: 'Cancelar pedido simulado',
    read_charge_count: 'Observar número de pagos',
    done: 'Objetivo del modelo alcanzado',
    branch: 'Observación',
    charges: 'pagos iniciales',
    modelCost: 'coste',
  },
};
const lang = new URLSearchParams(location.search).get('lang') || 'en',
  m = messages[lang] || messages.en;
document.documentElement.lang = messages[lang] ? lang : 'en';
document.querySelectorAll('[data-i18n]').forEach((x) => (x.textContent = m[x.dataset.i18n]));
document.querySelectorAll('nav a').forEach((a) => {
  if (a.textContent.toLowerCase() === document.documentElement.lang)
    a.setAttribute('aria-current', 'page');
});
const $ = (id) => document.getElementById(id),
  el = (tag, text, cls) => {
    const x = document.createElement(tag);
    if (text !== undefined) x.textContent = text;
    if (cls) x.className = cls;
    return x;
  };
let initial, report;
function renderNode(node) {
  const box = el('div', undefined, 'plan-node');
  if (node.kind === 'done') {
    box.append(el('div', m.done, 'done-node'));
    return box;
  }
  box.append(
    el('div', m[node.id] || node.id, node.kind === 'observe' ? 'observe-node' : 'action-node'),
  );
  if (node.kind === 'action') box.append(renderNode(node.next));
  else {
    const branches = el('div', undefined, 'branches');
    for (const b of node.branches) {
      const branch = el('div', undefined, 'branch');
      branch.append(
        el(
          'p',
          m.branch +
            ' · ' +
            Object.entries(b.value)
              .map(([k, v]) => `${k}=${v}`)
              .join(', '),
          'branch-title',
        ),
        renderNode(b.plan),
      );
      branches.append(branch);
    }
    box.append(branches);
  }
  return box;
}
function render(result) {
  report = result;
  $('worlds').textContent = result.worlds.length;
  $('cost').textContent = result.worst_case_cost ?? '—';
  $('verified').textContent = result.verification?.valid ? m.valid : '—';
  $('verdict').textContent = result.plan
    ? result.minimum_cost_within_depth_proven
      ? m.optimal
      : m.feasible
    : m.review;
  $('digest').textContent = result.snapshot_sha256;
  $('tree').replaceChildren();
  $('replays').replaceChildren();
  if (result.plan) {
    $('tree').append(renderNode(result.plan));
    for (const p of result.verification.paths) {
      const row = el('div', undefined, 'replay');
      row.append(
        el('strong', `${p.initial_world.net_charges} ${m.charges}`),
        el(
          'span',
          p.steps.map((s) => m[s.action || s.observe] || s.action || s.observe).join(' → '),
        ),
        el('code', m.modelCost + ' ' + p.cost),
      );
      $('replays').append(row);
    }
    $('status').textContent = m.ready;
  } else {
    $('tree').append(el('p', m[result.reason] || m.review, 'review-reason'));
    if (result.witness) $('tree').append(el('pre', JSON.stringify(result.witness, null, 2)));
    $('status').textContent = m.review;
  }
}
async function run() {
  $('plan').disabled = true;
  $('status').textContent = m.busy;
  try {
    const caseData = structuredClone(initial);
    caseData.trace = caseData.trace.filter((t) => t.operation !== 'charge_attempt');
    for (let i = 0; i < Number($('attempts').value); i++)
      caseData.trace.push({ operation: 'charge_attempt', status: 'unknown' });
    if (!$('observe').checked) caseData.observations = [];
    if ($('irreversible').checked)
      caseData.trace.push({ operation: 'send_notification', status: 'confirmed' });
    const response = await fetch('/api/plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case: caseData, max_depth: Number($('depth').value) }),
    });
    if (!response.ok) throw Error();
    render(await response.json());
  } catch {
    $('status').textContent = m.error;
  } finally {
    $('plan').disabled = false;
  }
}
$('plan').addEventListener('click', run);
$('download').addEventListener('click', () => {
  if (!report) return;
  const url = URL.createObjectURL(
      new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' }),
    ),
    a = el('a');
  a.href = url;
  a.download = 'compensation-plan-evidence.json';
  a.click();
  URL.revokeObjectURL(url);
});
try {
  const response = await fetch('/api/example');
  if (!response.ok) throw Error();
  initial = await response.json();
  await run();
} catch {
  $('status').textContent = m.error;
}
