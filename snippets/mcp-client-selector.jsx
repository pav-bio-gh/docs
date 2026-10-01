// Install picker for the MCP server: one tile per client, each with the exact
// command, link or config that connects it. Every client here signs in with
// OAuth in the browser, so no API key appears on this card. Icon paths are from
// Simple Icons (CC0).
export const McpClientSelector = () => {
  const mcpUrl = "https://api.pav.bio/mcp";
  const cursorInstallUrl = `cursor://anysphere.cursor-deeplink/mcp/install?name=pav&config=${btoa(
    JSON.stringify({ url: mcpUrl })
  )}`;
  const icons = {
    "claude-code": "M21 10.5h3v3h-3v3h-1.5v3H18v-3h-1.5v3H15v-3H9v3H7.5v-3H6v3H4.5v-3H3v-3H0v-3h3v-6h18Zm-15 0h1.5v-3H6Zm10.5 0H18v-3h-1.5z",
    codex: "M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z",
    cursor: "M11.503.131 1.891 5.678a.84.84 0 0 0-.42.726v11.188c0 .3.162.575.42.724l9.609 5.55a1 1 0 0 0 .998 0l9.61-5.55a.84.84 0 0 0 .42-.724V6.404a.84.84 0 0 0-.42-.726L12.497.131a1.01 1.01 0 0 0-.996 0M2.657 6.338h18.55c.263 0 .43.287.297.515L12.23 22.918c-.062.107-.229.064-.229-.06V12.335a.59.59 0 0 0-.295-.51l-9.11-5.257c-.109-.063-.064-.23.061-.23",
    opencode: "M22 24H2V0h20zM17 4.8H7v14.4h10z"
  };
  const clients = [
    {
      id: "claude-code",
      name: "Claude Code",
      detail: "Run in terminal",
      codeLabel: "Terminal",
      code: `claude mcp add --transport http pav ${mcpUrl}`,
      description: "Run this in your terminal to add Pav to Claude Code.",
      hint: (
        <>
          Then enter <code>/mcp</code> in Claude Code, choose <strong>pav</strong>, and
          complete the browser sign-in.
        </>
      )
    },
    {
      id: "codex",
      name: "Codex",
      detail: "Run in terminal",
      codeLabel: "Terminal",
      code: `codex mcp add pav --url ${mcpUrl}`,
      description: "Run this in your terminal. Codex opens the browser sign-in right away.",
      hint: (
        <>
          Then enter <code>/mcp</code> in Codex and confirm <strong>pav</strong> is connected.
        </>
      )
    },
    {
      id: "cursor",
      name: "Cursor",
      detail: "One click",
      codeLabel: "mcp.json",
      code: JSON.stringify({ mcpServers: { pav: { url: mcpUrl } } }, null, 2),
      installUrl: cursorInstallUrl,
      description: "Install in one click, or add this to your Cursor MCP config.",
      hint: (
        <>
          Open <strong>Cursor Settings</strong>, select <strong>MCP</strong>, and complete the
          Pav sign-in.
        </>
      )
    },
    {
      id: "opencode",
      name: "OpenCode",
      detail: "Copy config",
      codeLabel: "opencode.json",
      code: JSON.stringify(
        {
          $schema: "https://opencode.ai/config.json",
          mcp: { pav: { type: "remote", url: mcpUrl, enabled: true } }
        },
        null,
        2
      ),
      description:
        "Add this to your global or project config. OpenCode opens the Pav sign-in in your browser on first use.",
      hint: (
        <>
          Sign in, then confirm <strong>pav</strong> is connected.
        </>
      )
    }
  ];

  const [activeId, setActiveId] = useState(clients[0].id);
  const [copiedKey, setCopiedKey] = useState(null);
  const tabRefs = useRef([]);
  const timeoutRef = useRef(null);
  useEffect(() => () => window.clearTimeout(timeoutRef.current), []);

  const copy = async (key, text) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      return;
    }
    window.clearTimeout(timeoutRef.current);
    setCopiedKey(key);
    timeoutRef.current = window.setTimeout(() => setCopiedKey(null), 2000);
  };

  const onTabKeyDown = (event, index) => {
    const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
    if (!step) {
      return;
    }
    event.preventDefault();
    const next = (index + step + clients.length) % clients.length;
    setActiveId(clients[next].id);
    tabRefs.current[next]?.focus();
  };

  const CopyButton = ({ copyKey, text, label }) => (
    <button
      type="button"
      className="pav-mcp-copy"
      onClick={() => copy(copyKey, text)}
      aria-label={`Copy ${label}`}
    >
      {copiedKey === copyKey ? (
        <svg aria-hidden="true" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M20 6 9 17l-5-5" />
        </svg>
      ) : (
        <svg aria-hidden="true" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect width="14" height="14" x="8" y="8" rx="2" />
          <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
        </svg>
      )}
      <span>{copiedKey === copyKey ? "Copied" : "Copy"}</span>
    </button>
  );

  const active = clients.find((client) => client.id === activeId);

  return (
    <div className="pav-mcp not-prose">
      <div className="pav-mcp-tabs" role="tablist" aria-label="MCP client">
        {clients.map((client, index) => (
          <button
            key={client.id}
            ref={(node) => {
              tabRefs.current[index] = node;
            }}
            type="button"
            role="tab"
            id={`pav-mcp-tab-${client.id}`}
            aria-selected={client.id === activeId}
            aria-controls="pav-mcp-panel"
            tabIndex={client.id === activeId ? 0 : -1}
            className="pav-mcp-tab"
            onClick={() => setActiveId(client.id)}
            onKeyDown={(event) => onTabKeyDown(event, index)}
          >
            <svg aria-hidden="true" viewBox="0 0 24 24" className="pav-mcp-tab-icon">
              <path d={icons[client.id]} fill="currentColor" />
            </svg>
            <span className="pav-mcp-tab-name">{client.name}</span>
            <span className="pav-mcp-tab-detail">{client.detail}</span>
          </button>
        ))}
      </div>

      <div
        className="pav-mcp-panel"
        role="tabpanel"
        id="pav-mcp-panel"
        aria-labelledby={`pav-mcp-tab-${active.id}`}
      >
        <p className="pav-mcp-description">{active.description}</p>
        {active.installUrl ? (
          <a className="pav-mcp-install" href={active.installUrl}>
            Add to {active.name}
            <svg aria-hidden="true" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M5 12h14" />
              <path d="m12 5 7 7-7 7" />
            </svg>
          </a>
        ) : null}
        <div className="pav-mcp-code">
          <div className="pav-mcp-code-bar">
            <span>{active.codeLabel}</span>
            <CopyButton copyKey={active.id} text={active.code} label={active.codeLabel} />
          </div>
          <pre>
            <code>{active.code}</code>
          </pre>
        </div>
        <p className="pav-mcp-hint">{active.hint}</p>
      </div>

      <div className="pav-mcp-url">
        <p>Using another MCP client? Point it at:</p>
        <div className="pav-mcp-url-row">
          <code>{mcpUrl}</code>
          <CopyButton copyKey="url" text={mcpUrl} label="server URL" />
        </div>
      </div>
    </div>
  );
};
