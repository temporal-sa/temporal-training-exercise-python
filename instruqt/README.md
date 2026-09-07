# Temporal in Practice: Instruqt Track

The eight exercises in this repo, packaged as an Instruqt hands-on lab. Slug
`temporal-in-practice`, owner `temporal`.

Attendees get a container sandbox with a Temporal dev server already running,
the native code editor pointed at the exercise directory, and the finished
solution one tab away.

## Two subfolders

```
instruqt/
├── track/      The track definition. This is what `instruqt track push` uploads.
└── sandbox/    Sandbox provisioning and the files it stages at runtime.
```

There is **no sandbox image to build and no Dockerfile**. `config.yml` points
at stock `python:3.11` from Docker Hub and the sandbox provisions itself at lab
start. The only artifact that ever gets published is the track definition.

### The two setup scripts

Provisioning is split across the two folders:

| File | Ships with | Job |
|------|-----------|-----|
| `track/track_scripts/setup-workshop` | `instruqt track push` | Wait for bootstrap, clone the repo, hand off. Installs nothing. |
| `sandbox/setup-workshop` | the git clone | All the real provisioning |

The thin one does only what has to happen before the other file exists on
disk. It then `exec`s `/root/workshop/instruqt/sandbox/setup-workshop`.

> [!IMPORTANT]
> Edits to `sandbox/setup-workshop` do **not** take effect on `instruqt track
> push`. That file is read from the clone, so it has to be pushed to
> `WORKSHOP_REF` first. Only the thin track script travels with the track.

#### Why `track_scripts/` at all

`track_scripts/` is **optional**. `instruqt track validate` passes with the
directory absent, and there is no track-level `cleanup-workshop` here: the
container is destroyed at teardown and this track creates nothing outside it,
so killing processes on the way out would be dead code.

`setup-workshop` stays because it is the only hook that runs **once per
sandbox, before any challenge**. The alternative is per-challenge
`setup-workshop`, which breaks two ways here:

- `skipping_enabled: true` lets an attendee open challenge 5 first, so
  per-challenge provisioning would have to live in all eight, or in a shared
  script guarded by a sentinel.
- Hot Start warms a pool by provisioning sandboxes. Challenge setup runs when
  an attendee enters a challenge, which is after they have been handed a
  sandbox, so provisioning there would not be pre-warmed and challenge 1 would
  stall for minutes.

Anything in `track_scripts/` must be named for a host in `config.yml`.
`setup-wronghost` fails validation with `references unknown host`.

### `track/`

```
track/
├── track.yml                     Metadata, time limits, loading cards
├── config.yml                    Container sandbox: base image, memory, exposed ports
├── track_scripts/
│   └── setup-workshop            Thin bootstrap: clone, then hand off to sandbox/
├── 01-hello-temporal/            One directory per exercise, numbered sequentially
├── 02-signals/
├── 03-queries/
├── 04-search-attributes/
├── 05-activity-summaries/
├── 06-unit-testing/
├── 07-manual-retry/
└── 08-versioning/
    ├── assignment.md             Frontmatter (tabs, notes) + challenge body
    ├── setup-workshop            Runs when the challenge starts
    ├── check-workshop            Runs when the attendee clicks Check
    ├── solve-workshop            Runs on Skip and on `instruqt track test`
    └── cleanup-workshop          Runs when the challenge ends
```

Instruqt derives challenge order from directory sort order, so the `NN-`
prefixes have to stay sequential and `track.yml` must have no `challenges:`
block. Lifecycle script filenames are suffixed with the hostname from
`config.yml` (`workshop`).

> [!WARNING]
> Instruqt parses every file inside a challenge directory as a lifecycle
> script. A stray diagram or image next to `assignment.md` breaks the track.
> Shared assets belong under `sandbox/` or inline in the markdown.

### `sandbox/`

```
sandbox/
├── README.md                     How to ship a sandbox change
├── setup-workshop                All the provisioning. See below.
└── proxy/                        Network control panel
    ├── toggle_addon.py           mitmproxy addon, re-reads state.json per request
    ├── controlpanel.py           Flask UI + REST API on port 5000
    ├── state.json                Default toggle state
    └── static/index.html         The toggle UI
```

These files reach the sandbox through the git clone the track script
performs, then get copied to `/root/proxy/` so the addon and the panel have a
writable `state.json`. Any ref you pin `WORKSHOP_REF` to therefore has to
contain `instruqt/sandbox/proxy/`; the setup script fails with an explicit
message if it does not.

## What provisioning does

`track/track_scripts/setup-workshop` waits for the Instruqt bootstrap marker,
clones this repo to `/root/workshop`, and hands off. It installs nothing: the
base image already ships `git`, which is the only binary a clone needs. Then
`sandbox/setup-workshop` does the work, in order:

1. System packages the base image lacks: `jq`, `less`, `vim-tiny`, `nano`,
   `bash-completion`.
2. `uv`, installed to `/usr/local/bin`. No interpreter download, because
   `python:3.11` already satisfies `.python-version`.
3. The Temporal CLI, symlinked to `/usr/local/bin/temporal`.
4. `uv sync --frozen` in `/root/workshop`.
5. mitmproxy and Flask into `/opt/proxy-venv`, plus the mitmproxy CA cert
   trusted system-wide and appended to the workshop venv's certifi bundle.
6. The network control panel staged to `/root/proxy/`.
7. Shell environment written to `/etc/profile.d/workshop.sh`.
8. mitmproxy, the control panel, and `temporal server start-dev` started in the
   background, then a health wait.
9. The exercise 8 replay history seeded from `solution8/`.

### What this costs

All of it runs at sandbox provision time. Measured at about 30 seconds on
`python:3.11`, against roughly ten for a fully baked image, so the gap is
small and **Hot Start absorbs it entirely** (see below). What Hot Start does
not fix:

- **No version pinning by default.** `WORKSHOP_REF` defaults to `main`, and
  apt, `uv`, and the Temporal CLI installer all resolve to whatever is current
  when the sandbox is provisioned. **Pin `WORKSHOP_REF` to a tag or commit
  before a live workshop**, so a pool warmed at 9am and one warmed at 11am
  contain the same code.
- **No warm caches.** The first `uv run` in each challenge is a cold start.
- **Sensitive to upstream blips.** Debian mirrors, GitHub, PyPI, and
  `temporal.download` are all in the critical path. A failure in any of them
  while a pool is warming produces broken sandboxes in the pool.

If provisioning time or reproducibility becomes a real problem, the fix is to
move steps 1 through 5 into a Dockerfile, publish the image, and point
`config.yml` at it. `sandbox/setup-workshop` then shrinks to steps 6 through 9,
and the split already isolates that change to one file.

### Hot Start

Hot Start pre-provisions a pool of sandboxes before the session and hands one
out instantly when an attendee clicks Start. It is the supported mechanism for
more than roughly five simultaneous starts; without it, ~30 concurrent starts
hit `Failed to start track`. It also means nobody waits on the provisioning
above, because it already ran.

It is a web-UI setting with no CLI equivalent, so it cannot live in
`track.yml`. Enable it under Track Settings, size the pool to expected
attendees plus a 10 to 20 percent buffer, and trigger warm-up well ahead of
the session.

Three things to watch that are specific to provisioning at lab start rather
than baking an image:

- **A warm pool holds a snapshot of whatever `WORKSHOP_REF` pointed at when it
  was warmed.** Push an exercise fix after warm-up and pooled sandboxes keep
  serving the old clone. Re-warm the pool after any code change you need
  attendees to see.
- **The dev server in a pooled sandbox has been running since warm-up.** It is
  a SQLite dev server with no data that matters, so this is fine, but any
  workflow you start while validating a pooled sandbox is visible to whoever
  gets handed that sandbox.
- **Disable Hot Start after the session.** Pre-provisioned sandboxes cost money
  while idle.

### Where a dependency belongs

The base image supplies only what the **clone** needs, because the track script
runs before `sandbox/setup-workshop` exists on disk. `python:3.11` was picked
for exactly that: `git`, `curl`, `unzip`, `gcc` with build headers,
`update-ca-certificates`, and a 3.11 interpreter that matches
`.python-version`.

Everything else goes in step 1 of `sandbox/setup-workshop`. Dropping the
interpreter download and the `python3`/`build-essential` apt install took
provisioning from a few minutes to about 30 seconds.

`instruqt/sandbox/README.md` has the decision table and how to vet a
replacement base image.

### Two things that are easy to break

**Toolchain on the default PATH.** `uv` and `temporal` are installed to
`/usr/local/bin` on purpose. Check and solve scripts run non-interactively and
never source a profile, so anything reachable only via `PATH` export in a
profile is invisible to them.

**Proxy and cert variables.** They live in `/etc/profile.d/workshop.sh`, with
`/etc/bash.bashrc` sourcing it for interactive non-login shells, which is what
Instruqt's terminal tabs open. Putting them only in `/etc/bash.bashrc` does
not work: Ubuntu's `/root/.bashrc` returns early for non-interactive shells.
The symptom is subtle, because the toggles appear to do nothing when traffic
never reaches the proxy.

**Search attributes.** The dev server starts with
`--search-attribute AccountId=Text`, which exercise 4 needs. Without that flag
the `upsert_search_attributes` call fails the Workflow Task, and the Workflow
just stops making progress.

## Network control panel

Ported from [temporal-sa/ai-agents-webinar](https://github.com/temporal-sa/ai-agents-webinar).
mitmproxy listens on `127.0.0.1:8888`, every shell routes outbound HTTP and
HTTPS through it, and a Flask panel on port 5000 flips toggles by writing
`state.json`. The addon re-reads that file on every request, so a toggle takes
effect immediately with no restart.

| Toggle | Hosts | Effect when off |
|--------|-------|-----------------|
| `pypi` | `pypi.org`, `files.pythonhosted.org` | `uv` cannot reach the package index |
| `github` | `github.com`, `raw.githubusercontent.com`, `codeload.github.com` | Git and release downloads fail |
| `httpbin` | `httpbin.org` | A request-echo endpoint for proving the proxy is in the path |
| Kill switch | everything | HTTP 503 on all outbound traffic |

`NO_PROXY=127.0.0.1,localhost` keeps the Temporal SDK's gRPC traffic and the
dev server's own HTTP off the proxy, so flipping the kill switch never breaks
the lab itself.

These eight exercises call no external HTTP APIs of their own. Their Activities
simulate failure locally, so the toggles do not disrupt any Workflow as
shipped. The panel is wired and ready for a chapter that does hit a real API,
and it makes a usable instructor demo as-is: flip `pypi` off, run `uv sync`,
watch it fail, flip it back.

To add a toggle: add the key and its hostnames to `SERVICE_HOSTS` in
`toggle_addon.py`, add the key to `state.json`, and add a display label to
`SERVICE_LABELS` in `controlpanel.py`. The UI renders itself from
`SERVICE_LABELS`, so there is no HTML to edit.

## Tabs

Every challenge has the same six tabs, in the same order, so the `tab-N`
references in the assignment bodies stay stable. Tab indexing is 0-based.

| Index | Tab | Type | Points at |
|-------|-----|------|-----------|
| `tab-0` | Code Editor | `code` | `/root/workshop/exerciseN` |
| `tab-1` | Worker | `terminal` | `/root/workshop` |
| `tab-2` | Terminal | `terminal` | `/root/workshop` |
| `tab-3` | Temporal UI | `service` | port 8233 |
| `tab-4` | Solution | `code` | `/root/workshop/solutionN` |
| `tab-5` | Network Control Panel | `service` | port 5000 |

Challenge 07 adds a seventh tab, **Signals** (`tab-6`), because its starter
blocks in `tab-2` while the attendee sends the retry Signal.

Terminals sit at `/root/workshop` because the exercises are one `uv` project
rooted there and every command runs as `uv run exerciseN/...` from the root.

Every port a tab points at has to be listed under `ports:` in `config.yml`.
Instruqt's proxy returns HTTP 572 for anything not listed.

## Challenge map

All eight are fill-in-the-blanks: the attendee edits code, and the check script
gates on the TODOs being gone plus a real outcome in Temporal.

| Challenge | Exercise | Checks |
|-----------|----------|--------|
| `01-hello-temporal` | 1 | TODOs gone, Workflow completed on `hello-task-queue` |
| `02-signals` | 2 | TODOs gone, `@workflow.signal` present, transfer completed |
| `03-queries` | 3 | TODOs gone, `@workflow.query` present, transfer completed |
| `04-search-attributes` | 4 | `upsert_search_attributes` called, execution findable by `AccountId` |
| `05-activity-summaries` | 5 | All three Activities carry `summary=`, transfer completed |
| `06-unit-testing` | 6 | TODOs gone, `pytest exercise6/` passes (7 tests) |
| `07-manual-retry` | 7 | `non_retryable` raised, retry loop waits on a Signal, transfer completed |
| `08-versioning` | 8 | `workflow.patched()` gates the new Activity, both tests pass including replay |

Solve scripts copy the matching `solutionN/` files into `exerciseN/` and then
drive a Workflow to completion, so `instruqt track test` exercises the whole
track end to end and Skip leaves the next challenge in a sane state.

## Publishing the track

All track commands run from `instruqt/track/`. Authenticate once with
`instruqt auth login`.

A push targets an **existing** track, so the slug has to be registered first.
Do that once, ever, from a throwaway directory so the upstream scaffold does
not overwrite the files here:

```bash
mkdir /tmp/scaffold && cd /tmp/scaffold
instruqt track create temporal-in-practice --title "Temporal in Practice"
cd - && rm -rf /tmp/scaffold
```

Then the first push, which needs `--force` to reconcile the backend-only
fields `create` populated:

```bash
cd instruqt/track
instruqt track push --force
instruqt track pull        # populates the track id and every tab id
cd -
git add instruqt/track/ && git commit -m "Pin Instruqt track and tab ids"
```

Afterwards:

```bash
cd instruqt/track
instruqt track validate    # local validation, no push
instruqt track push        # publish
instruqt track pull        # ids for any new challenge or tab, then commit
instruqt track test        # runs every solve script in order, end to end
```

`instruqt track diff` is absent from some CLI versions. If it errors as an
unknown command, compare with `instruqt track checksum` instead.

[.github/workflows/push-track.yml](../.github/workflows/push-track.yml)
validates and pushes automatically on merge to `main`. It needs a repo secret
named `INSTRUQT_TOKEN` holding an Instruqt org API key.

> [!IMPORTANT]
> Never edit the track in the Instruqt web UI while editing locally. It
> corrupts the `.remote` cache. Use the CLI exclusively. A handful of settings
> are web-UI authoritative regardless of what you push: `idle_timeout`, Hot
> Start, and invite configuration.

`instruqt track push` rewrites `track.yml` and each `assignment.md`
**frontmatter** in place: comments stripped, keys reordered, block scalars
collapsed, `checksum` injected. The first-push diff is large and that is
expected. Commit it as-is rather than prettifying it, and keep durable
explanation in this README instead of in YAML comments. `config.yml` is left
alone.

## Testing the sandbox locally

Static validation misses runtime bugs. For any change to either setup script
or to a command in an assignment, boot a container and walk the affected
challenge. This is the only way to test `sandbox/setup-workshop` before
pushing it, since `instruqt track push` does not carry that file.

Boot stock Ubuntu and provision it the way Instruqt does. The host ports are
offset because 7233 is usually a local dev server and 5000 is macOS AirPlay
Receiver. `sleep infinity` keeps stock Ubuntu alive without a TTY; Instruqt
supplies its own long-running command, so that is a local-only concern.

```bash
docker rm -f instruqt-test 2>/dev/null
docker run -d --name instruqt-test --platform linux/amd64 \
  -p 7299:7233 -p 8299:8233 -p 5099:5000 \
  python:3.11 sleep infinity

# Fake Instruqt's bootstrap marker, which setup-workshop waits on.
docker exec instruqt-test mkdir -p /opt/instruqt/bootstrap
docker exec instruqt-test touch /opt/instruqt/bootstrap/host-bootstrap-completed
```

To test your **local working tree**, seed `/root/workshop` first. The track
script skips its clone when that directory already exists, so it hands off to
your uncommitted `sandbox/setup-workshop`:

```bash
docker exec instruqt-test mkdir -p /root/workshop
tar --exclude='./.git' --exclude='./.venv' --exclude='./.pytest_cache' \
    --exclude='__pycache__' -cf - . \
  | docker exec -i instruqt-test tar -xf - -C /root/workshop
```

Then provision. Omit the seeding step above to test the clone path an attendee
actually gets, in which case `WORKSHOP_REF` has to be a pushed ref:

```bash
docker cp instruqt/track/track_scripts/setup-workshop instruqt-test:/tmp/setup-workshop
docker exec instruqt-test chmod +x /tmp/setup-workshop
docker exec -e WORKSHOP_REF=main instruqt-test /tmp/setup-workshop
```

Temporal UI lands on <http://localhost:8299> and the control panel on
<http://localhost:5099>.

Walk one challenge's lifecycle scripts:

```bash
CH=04-search-attributes
docker exec instruqt-test mkdir -p /tmp/ch
for s in setup check solve cleanup; do
  docker cp "instruqt/track/$CH/$s-workshop" "instruqt-test:/tmp/ch/$s"
done
docker exec instruqt-test chmod -R +x /tmp/ch
docker exec instruqt-test /tmp/ch/setup
docker exec instruqt-test /tmp/ch/solve
docker exec instruqt-test /tmp/ch/check
docker exec instruqt-test /tmp/ch/cleanup
```

Tear down:

```bash
docker rm -f instruqt-test
```

## Time limits

`timelimit: 14400` (4 hours) budgets 30 minutes per coding challenge across
eight challenges. `idle_timeout: 3600` lets sandboxes survive a break.
Attendees extend in-session in 15 minute increments.

Both are tuned for a self-paced run. A live instructor-led session usually
wants `feedback_recap_enabled` and `feedback_tab_enabled` set to `false`,
because feedback gets collected out of band.

## Live workshop pre-flight

`track.yml` sets `maintenance: true`, so only owners and authors can launch it.
Flip it to `false` and push when the track is ready. Everything else here is a
web-UI or by-hand step that no push can set for you.

- [ ] **`WORKSHOP_REF` pinned** to a tag or commit in
      `track/track_scripts/setup-workshop`. Without this a pool warmed at
      different times contains different code.
- [ ] **`sandbox/setup-workshop` pushed** to that ref. It is read from the
      clone, so an unpushed edit to it has no effect no matter how many times
      you push the track.
- [ ] **Hot Start enabled**, pool sized to expected attendees plus 10 to 20
      percent, warmed well ahead of the session. Required above roughly five
      simultaneous starts.
- [ ] **Pool re-warmed** after any exercise or sandbox change made since the
      last warm-up.
- [ ] **`idle_timeout` set in the web UI** (Track, Settings, Additional
      Settings) to workshop length plus 20 minutes. The `track.yml` value is
      used at track creation and the web UI wins afterwards, so a pushed
      `3600` can still show as `600`.
- [ ] **`feedback_recap_enabled` and `feedback_tab_enabled` set to `false`**
      in `track.yml` if feedback is collected out of band. They are `true`
      today, which suits a self-paced run.
- [ ] **Invite configured to collect the attendee name**, if you want a
      readable `INSTRUQT_USER_NAME` rather than the opaque participant ID.
- [ ] **`instruqt track test` passes.** Runs every solve script in order and
      catches regressions a manual click-through misses.
- [ ] **`INSTRUQT_TOKEN` repo secret exists**, or CI cannot push.

After the session:

- [ ] **Disable Hot Start** if the pool was sized for this session only.
      Pre-provisioned sandboxes cost money while idle.
- [ ] **Reset `idle_timeout`** if you raised it and the track ships as
      self-paced afterwards.

No `secrets:` are declared in `config.yml`, so there is nothing to populate
under Track Settings, Secrets.

## Known issues

Quirks of the exercise code that the track works around rather than fixes.
Worth cleaning up in the exercises themselves.

- **`exercise7` mixes import styles.** `start_worker.py` and
  `start_workflow.py` use package-relative imports while
  `money_transfer_workflow.py` imports by bare name. Neither
  `uv run exercise7/start_worker.py` nor
  `uv run python -m exercise7.start_worker` works on its own. The assignment
  uses `PYTHONPATH=exercise7 uv run python -m exercise7.start_worker`.
- **`exercise8` and `solution8` tests need `PYTHONPATH`.** They import by bare
  name but sit in a package (`__init__.py` present), so pytest puts the repo
  root on `sys.path` and the imports fail. The command documented in
  `exercise8/README.md` fails as written. The assignment prefixes
  `PYTHONPATH=exercise8`.
- **`exercise6/README.md` references `run_tests.py`,** which exists only in
  `solution6/`. The assignment uses `uv run pytest exercise6/ -v`.
- **`exercise5/start_workflow.py` suggests `memo={"summary": ...}`** for the
  execution summary. `static_summary=` on `client.start_workflow` is the field
  the Web UI renders as the execution title, and `solution5` implements
  neither. The assignment tells attendees to use `static_summary=`.
- **Task queue names are inconsistent** across exercises:
  `MoneyTransferTaskQueue` in exercises 2 through 5,
  `money-transfer-task-queue` in `solution5`, exercise 7 and exercise 8. The
  check scripts accept both.
- **`exercise8/workflow_history_v1.json` is not in the repo.** Task 4 of that
  exercise asks the attendee to generate it. Both
  `track_scripts/setup-workshop` and the challenge's own `setup-workshop` seed
  it from `solution8/` so the replay test runs without that detour.

## Undocumented `track.yml` fields

`track.yml` uses only documented fields. If you add `hideStopButton` or
`enhanced_loading`, note that neither appears in Instruqt's published
`lab_config` schema even though both work in production.
