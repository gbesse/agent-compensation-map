import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { readFile } from 'node:fs/promises';
import assert from 'node:assert/strict';
const transport = new StdioClientTransport({
  command: process.env.PYTHON || 'python3',
  args: ['-m', 'compensation_map', 'mcp'],
  stderr: 'pipe',
});
const client = new Client({ name: 'compensation-map-sdk-check', version: '1.0.0' });
try {
  await client.connect(transport);
  const listed = await client.listTools();
  assert.equal(listed.tools.length, 1);
  assert.equal(listed.tools[0].annotations.readOnlyHint, true);
  const caseData = JSON.parse(
    await readFile('compensation_map/examples/ambiguous-charge.json', 'utf8'),
  );
  const result = await client.callTool({
    name: 'compensation_plan',
    arguments: { case: caseData },
  });
  assert.equal(result.isError, false);
  assert.equal(result.structuredContent.worst_case_cost, 9);
  assert.equal(result.structuredContent.verification.worlds_checked, 3);
  assert.equal(result.structuredContent.external_actions_executed, false);
  console.log(
    'Official MCP SDK: initialize, listTools and structured read-only callTool verified.',
  );
} finally {
  await client.close();
}
