# [Bump the github-actions group across 1 directory with 5 updates](https://github.com/bingdu748/Laboratory_of_Mad_Scientist/pull/13)

## 元信息

- 创建时间: 2026-06-09 15:52:58
- 更新时间: 2026-06-10 00:32:46

## 内容

Bumps the github-actions group with 5 updates in the / directory:

| Package | From | To |
| --- | --- | --- |
| [actions/checkout](https://github.com/actions/checkout) | `4.2.2` | `6.0.3` |
| [actions/setup-python](https://github.com/actions/setup-python) | `5.3.0` | `6.2.0` |
| [actions/configure-pages](https://github.com/actions/configure-pages) | `5` | `6` |
| [actions/upload-pages-artifact](https://github.com/actions/upload-pages-artifact) | `3` | `5` |
| [actions/deploy-pages](https://github.com/actions/deploy-pages) | `4.1.5` | `5.0.0` |


Updates `actions/checkout` from 4.2.2 to 6.0.3
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/actions/checkout/releases">actions/checkout's releases</a>.</em></p>
<blockquote>
<h2>v6.0.3</h2>
<h2>What's Changed</h2>
<ul>
<li>Update changelog by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2357">actions/checkout#2357</a></li>
<li>fix: expand merge commit SHA regex and add SHA-256 test cases by <a href="https://github.com/yaananth"><code>@​yaananth</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2414">actions/checkout#2414</a></li>
<li>Fix checkout init for SHA-256 repositories by <a href="https://github.com/yaananth"><code>@​yaananth</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2439">actions/checkout#2439</a></li>
<li>Update changelog for v6.0.3 by <a href="https://github.com/yaananth"><code>@​yaananth</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2446">actions/checkout#2446</a></li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a href="https://github.com/yaananth"><code>@​yaananth</code></a> made their first contribution in <a href="https://redirect.github.com/actions/checkout/pull/2414">actions/checkout#2414</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/actions/checkout/compare/v6...v6.0.3">https://github.com/actions/checkout/compare/v6...v6.0.3</a></p>
<h2>v6.0.2</h2>
<h2>What's Changed</h2>
<ul>
<li>Add orchestration_id to git user-agent when ACTIONS_ORCHESTRATION_ID is set by <a href="https://github.com/TingluoHuang"><code>@​TingluoHuang</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2355">actions/checkout#2355</a></li>
<li>Fix tag handling: preserve annotations and explicit fetch-tags by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2356">actions/checkout#2356</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/actions/checkout/compare/v6.0.1...v6.0.2">https://github.com/actions/checkout/compare/v6.0.1...v6.0.2</a></p>
<h2>v6.0.1</h2>
<h2>What's Changed</h2>
<ul>
<li>Update all references from v5 and v4 to v6 by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2314">actions/checkout#2314</a></li>
<li>Add worktree support for persist-credentials includeIf by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2327">actions/checkout#2327</a></li>
<li>Clarify v6 README by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2328">actions/checkout#2328</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/actions/checkout/compare/v6...v6.0.1">https://github.com/actions/checkout/compare/v6...v6.0.1</a></p>
<h2>v6.0.0</h2>
<h2>What's Changed</h2>
<ul>
<li>Update README to include Node.js 24 support details and requirements by <a href="https://github.com/salmanmkc"><code>@​salmanmkc</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2248">actions/checkout#2248</a></li>
<li>Persist creds to a separate file by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2286">actions/checkout#2286</a></li>
<li>v6-beta by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2298">actions/checkout#2298</a></li>
<li>update readme/changelog for v6 by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2311">actions/checkout#2311</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/actions/checkout/compare/v5.0.0...v6.0.0">https://github.com/actions/checkout/compare/v5.0.0...v6.0.0</a></p>
<h2>v6-beta</h2>
<h2>What's Changed</h2>
<p>Updated persist-credentials to store the credentials under <code>$RUNNER_TEMP</code> instead of directly in the local git config.</p>
<p>This requires a minimum Actions Runner version of <a href="https://github.com/actions/runner/releases/tag/v2.329.0">v2.329.0</a> to access the persisted credentials for <a href="https://docs.github.com/en/actions/tutorials/use-containerized-services/create-a-docker-container-action">Docker container action</a> scenarios.</p>
<h2>v5.0.1</h2>
<h2>What's Changed</h2>
<ul>
<li>Port v6 cleanup to v5 by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2301">actions/checkout#2301</a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/actions/checkout/blob/main/CHANGELOG.md">actions/checkout's changelog</a>.</em></p>
<blockquote>
<h2>v6.0.3</h2>
<ul>
<li>Fix checkout init for SHA-256 repositories by <a href="https://github.com/yaananth"><code>@​yaananth</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2439">actions/checkout#2439</a></li>
<li>fix: expand merge commit SHA regex and add SHA-256 test cases by <a href="https://github.com/yaananth"><code>@​yaananth</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2414">actions/checkout#2414</a></li>
</ul>
<h2>v6.0.2</h2>
<ul>
<li>Fix tag handling: preserve annotations and explicit fetch-tags by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2356">actions/checkout#2356</a></li>
</ul>
<h2>v6.0.1</h2>
<ul>
<li>Add worktree support for persist-credentials includeIf by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2327">actions/checkout#2327</a></li>
</ul>
<h2>v6.0.0</h2>
<ul>
<li>Persist creds to a separate file by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2286">actions/checkout#2286</a></li>
<li>Update README to include Node.js 24 support details and requirements by <a href="https://github.com/salmanmkc"><code>@​salmanmkc</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2248">actions/checkout#2248</a></li>
</ul>
<h2>v5.0.1</h2>
<ul>
<li>Port v6 cleanup to v5 by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2301">actions/checkout#2301</a></li>
</ul>
<h2>v5.0.0</h2>
<ul>
<li>Update actions checkout to use node 24 by <a href="https://github.com/salmanmkc"><code>@​salmanmkc</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2226">actions/checkout#2226</a></li>
</ul>
<h2>v4.3.1</h2>
<ul>
<li>Port v6 cleanup to v4 by <a href="https://github.com/ericsciple"><code>@​ericsciple</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2305">actions/checkout#2305</a></li>
</ul>
<h2>v4.3.0</h2>
<ul>
<li>docs: update README.md by <a href="https://github.com/motss"><code>@​motss</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/1971">actions/checkout#1971</a></li>
<li>Add internal repos for checking out multiple repositories by <a href="https://github.com/mouismail"><code>@​mouismail</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/1977">actions/checkout#1977</a></li>
<li>Documentation update - add recommended permissions to Readme by <a href="https://github.com/benwells"><code>@​benwells</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2043">actions/checkout#2043</a></li>
<li>Adjust positioning of user email note and permissions heading by <a href="https://github.com/joshmgross"><code>@​joshmgross</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2044">actions/checkout#2044</a></li>
<li>Update README.md by <a href="https://github.com/nebuk89"><code>@​nebuk89</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2194">actions/checkout#2194</a></li>
<li>Update CODEOWNERS for actions by <a href="https://github.com/TingluoHuang"><code>@​TingluoHuang</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2224">actions/checkout#2224</a></li>
<li>Update package dependencies by <a href="https://github.com/salmanmkc"><code>@​salmanmkc</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/2236">actions/checkout#2236</a></li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/actions/checkout/commit/df4cb1c069e1874edd31b4311f1884172cec0e10"><code>df4cb1c</code></a> Update changelog for v6.0.3 (<a href="https://redirect.github.com/actions/checkout/issues/2446">#2446</a>)</li>
<li><a href="https://github.com/actions/checkout/commit/1cce3390c2bfda521930d01229c073c7ff920824"><code>1cce339</code></a> Fix checkout init for SHA-256 repositories (<a href="https://redirect.github.com/actions/checkout/issues/2439">#2439</a>)</li>
<li><a href="https://github.com/actions/checkout/commit/900f2210b1d28bbbd0bd22d17926b9e224e8f231"><code>900f221</code></a> fix: expand merge commit SHA regex and add SHA-256 test cases (<a href="https://redirect.github.com/actions/checkout/issues/2414">#2414</a>)</li>
<li><a href="https://github.com/actions/checkout/commit/0c366fd6a839edf440554fa01a7085ccba70ac98"><code>0c366fd</code></a> Update changelog (<a href="https://redirect.github.com/actions/checkout/issues/2357">#2357</a>)</li>
<li><a href="https://github.com/actions/checkout/commit/de0fac2e4500dabe0009e67214ff5f5447ce83dd"><code>de0fac2</code></a> Fix tag handling: preserve annotations and explicit fetch-tags (<a href="https://redirect.github.com/actions/checkout/issues/2356">#2356</a>)</li>
<li><a href="https://github.com/actions/checkout/commit/064fe7f3312418007dea2b49a19844a9ee378f49"><code>064fe7f</code></a> Add orchestration_id to git user-agent when ACTIONS_ORCHESTRATION_ID is set (...</li>
<li><a href="https://github.com/actions/checkout/commit/8e8c483db84b4bee98b60c0593521ed34d9990e8"><code>8e8c483</code></a> Clarify v6 README (<a href="https://redirect.github.com/actions/checkout/issues/2328">#2328</a>)</li>
<li><a href="https://github.com/actions/checkout/commit/033fa0dc0b82693d8986f1016a0ec2c5e7d9cbb1"><code>033fa0d</code></a> Add worktree support for persist-credentials includeIf (<a href="https://redirect.github.com/actions/checkout/issues/2327">#2327</a>)</li>
<li><a href="https://github.com/actions/checkout/commit/c2d88d3ecc89a9ef08eebf45d9637801dcee7eb5"><code>c2d88d3</code></a> Update all references from v5 and v4 to v6 (<a href="https://redirect.github.com/actions/checkout/issues/2314">#2314</a>)</li>
<li><a href="https://github.com/actions/checkout/commit/1af3b93b6815bc44a9784bd300feb67ff0d1eeb3"><code>1af3b93</code></a> update readme/changelog for v6 (<a href="https://redirect.github.com/actions/checkout/issues/2311">#2311</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/actions/checkout/compare/v4.2.2...v6.0.3">compare view</a></li>
</ul>
</details>
<br />

Updates `actions/setup-python` from 5.3.0 to 6.2.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/actions/setup-python/releases">actions/setup-python's releases</a>.</em></p>
<blockquote>
<h2>v6.2.0</h2>
<h2>What's Changed</h2>
<h3>Dependency Upgrades</h3>
<ul>
<li>Upgrade dependencies to Node 24 compatible versions by <a href="https://github.com/salmanmkc"><code>@​salmanmkc</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1259">actions/setup-python#1259</a></li>
<li>Upgrade urllib3 from 2.5.0 to 2.6.3 in <code>/__tests__/data</code> by <a href="https://github.com/dependabot"><code>@​dependabot</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1253">actions/setup-python#1253</a> and <a href="https://redirect.github.com/actions/setup-python/pull/1264">actions/setup-python#1264</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/actions/setup-python/compare/v6...v6.2.0">https://github.com/actions/setup-python/compare/v6...v6.2.0</a></p>
<h2>v6.1.0</h2>
<h2>What's Changed</h2>
<h3>Enhancements:</h3>
<ul>
<li>Add support for <code>pip-install</code> input by <a href="https://github.com/gowridurgad"><code>@​gowridurgad</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1201">actions/setup-python#1201</a></li>
<li>Add graalpy early-access and windows builds by <a href="https://github.com/timfel"><code>@​timfel</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/880">actions/setup-python#880</a></li>
</ul>
<h3>Dependency and Documentation updates:</h3>
<ul>
<li>Enhanced wording and updated example usage for <code>allow-prereleases</code> by <a href="https://github.com/yarikoptic"><code>@​yarikoptic</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/979">actions/setup-python#979</a></li>
<li>Upgrade urllib3 from 1.26.19 to 2.5.0 and document breaking changes in v6 by <a href="https://github.com/dependabot"><code>@​dependabot</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1139">actions/setup-python#1139</a></li>
<li>Upgrade typescript from 5.4.2 to 5.9.3 and Documentation update by <a href="https://github.com/dependabot"><code>@​dependabot</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1094">actions/setup-python#1094</a></li>
<li>Upgrade actions/publish-action from 0.3.0 to 0.4.0 &amp; Documentation update for pip-install input by <a href="https://github.com/dependabot"><code>@​dependabot</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1199">actions/setup-python#1199</a></li>
<li>Upgrade requests from 2.32.2 to 2.32.4 by <a href="https://github.com/dependabot"><code>@​dependabot</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1130">actions/setup-python#1130</a></li>
<li>Upgrade prettier from 3.5.3 to 3.6.2 by <a href="https://github.com/dependabot"><code>@​dependabot</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1234">actions/setup-python#1234</a></li>
<li>Upgrade <code>@​types/node</code> from 24.1.0 to 24.9.1 and update macos-13 to macos-15-intel by <a href="https://github.com/dependabot"><code>@​dependabot</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1235">actions/setup-python#1235</a></li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a href="https://github.com/yarikoptic"><code>@​yarikoptic</code></a> made their first contribution in <a href="https://redirect.github.com/actions/setup-python/pull/979">actions/setup-python#979</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/actions/setup-python/compare/v6...v6.1.0">https://github.com/actions/setup-python/compare/v6...v6.1.0</a></p>
<h2>v6.0.0</h2>
<h2>What's Changed</h2>
<h3>Breaking Changes</h3>
<ul>
<li>Upgrade to node 24 by <a href="https://github.com/salmanmkc"><code>@​salmanmkc</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1164">actions/setup-python#1164</a></li>
</ul>
<p>Make sure your runner is on version v2.327.1 or later to ensure compatibility with this release. <a href="https://github.com/actions/runner/releases/tag/v2.327.1">See Release Notes</a></p>
<h3>Enhancements:</h3>
<ul>
<li>Add support for <code>pip-version</code>  by <a href="https://github.com/priyagupta108"><code>@​priyagupta108</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1129">actions/setup-python#1129</a></li>
<li>Enhance reading from .python-version by <a href="https://github.com/krystof-k"><code>@​krystof-k</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/787">actions/setup-python#787</a></li>
<li>Add version parsing from Pipfile by <a href="https://github.com/aradkdj"><code>@​aradkdj</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1067">actions/setup-python#1067</a></li>
</ul>
<h3>Bug fixes:</h3>
<ul>
<li>Clarify pythonLocation behaviour for PyPy and GraalPy in environment variables by <a href="https://github.com/aparnajyothi-y"><code>@​aparnajyothi-y</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1183">actions/setup-python#1183</a></li>
<li>Change missing cache directory error to warning  by <a href="https://github.com/aparnajyothi-y"><code>@​aparnajyothi-y</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1182">actions/setup-python#1182</a></li>
<li>Add Architecture-Specific PATH Management for Python with --user Flag on Windows by <a href="https://github.com/aparnajyothi-y"><code>@​aparnajyothi-y</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1122">actions/setup-python#1122</a></li>
<li>Include python version in PyPy python-version output by <a href="https://github.com/cdce8p"><code>@​cdce8p</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1110">actions/setup-python#1110</a></li>
<li>Update docs: clarification on pip authentication with setup-python by <a href="https://github.com/priya-kinthali"><code>@​priya-kinthali</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1156">actions/setup-python#1156</a></li>
</ul>
<h3>Dependency updates:</h3>
<ul>
<li>Upgrade idna from 2.9 to 3.7 in /<strong>tests</strong>/data by <a href="https://github.com/dependabot"><code>@​dependabot</code></a>[bot] in <a href="https://redirect.github.com/actions/setup-python/pull/843">actions/setup-python#843</a></li>
<li>Upgrade form-data to fix critical vulnerabilities <a href="https://redirect.github.com/actions/setup-python/issues/182">#182</a> &amp; <a href="https://redirect.github.com/actions/setup-python/issues/183">#183</a> by <a href="https://github.com/aparnajyothi-y"><code>@​aparnajyothi-y</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1163">actions/setup-python#1163</a></li>
<li>Upgrade setuptools to 78.1.1 to fix path traversal vulnerability in PackageIndex.download by <a href="https://github.com/aparnajyothi-y"><code>@​aparnajyothi-y</code></a> in <a href="https://redirect.github.com/actions/setup-python/pull/1165">actions/setup-python#1165</a></li>
<li>Upgrade actions/checkout from 4 to 5 by <a href="https://github.com/dependabot"><code>@​dependabot</code></a>[bot] in <a href="https://redirect.github.com/actions/setup-python/pull/1181">actions/setup-python#1181</a></li>
<li>Upgrade <code>@​actions/tool-cache</code> from 2.0.1 to 2.0.2 by <a href="https://github.com/dependabot"><code>@​dependabot</code></a>[bot] in <a href="https://redirect.github.com/actions/setup-python/pull/1095">actions/setup-python#1095</a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/actions/setup-python/commit/a309ff8b426b58ec0e2a45f0f869d46889d02405"><code>a309ff8</code></a> Bump urllib3 from 2.6.0 to 2.6.3 in /<strong>tests</strong>/data (<a href="https://redirect.github.com/actions/setup-python/issues/1264">#1264</a>)</li>
<li><a href="https://github.com/actions/setup-python/commit/bfe8cc55a7890e3d6672eda6460ef37bfcc70755"><code>bfe8cc5</code></a> Upgrade <a href="https://github.com/actions"><code>@​actions</code></a> dependencies to Node 24 compatible versions (<a href="https://redirect.github.com/actions/setup-python/issues/1259">#1259</a>)</li>
<li><a href="https://github.com/actions/setup-python/commit/4f41a90a1f38628c7ccc608d05fbafe701bc20ae"><code>4f41a90</code></a> Bump urllib3 from 2.5.0 to 2.6.0 in /<strong>tests</strong>/data (<a href="https://redirect.github.com/actions/setup-python/issues/1253">#1253</a>)</li>
<li><a href="https://github.com/actions/setup-python/commit/83679a892e2d95755f2dac6acb0bfd1e9ac5d548"><code>83679a8</code></a> Bump <code>@​types/node</code> from 24.1.0 to 24.9.1 and update macos-13 to macos-15-intel ...</li>
<li><a href="https://github.com/actions/setup-python/commit/bfc4944b43a5d84377eca3cf6ab5b7992ba61923"><code>bfc4944</code></a> Bump prettier from 3.5.3 to 3.6.2 (<a href="https://redirect.github.com/actions/setup-python/issues/1234">#1234</a>)</li>
<li><a href="https://github.com/actions/setup-python/commit/97aeb3efb8a852c559869050c7fb175b4efcc8cf"><code>97aeb3e</code></a> Bump requests from 2.32.2 to 2.32.4 in /<strong>tests</strong>/data (<a href="https://redirect.github.com/actions/setup-python/issues/1130">#1130</a>)</li>
<li><a href="https://github.com/actions/setup-python/commit/443da59188462e2402e2942686db5aa6723f4bed"><code>443da59</code></a> Bump actions/publish-action from 0.3.0 to 0.4.0 &amp; Documentation update for pi...</li>
<li><a href="https://github.com/actions/setup-python/commit/cfd55ca82492758d853442341ad4d8010466803a"><code>cfd55ca</code></a> graalpy: add graalpy early-access and windows builds (<a href="https://redirect.github.com/actions/setup-python/issues/880">#880</a>)</li>
<li><a href="https://github.com/actions/setup-python/commit/bba65e51ff35d50c6dbaaacd8a4681db13aa7cb4"><code>bba65e5</code></a> Bump typescript from 5.4.2 to 5.9.3 and update docs/advanced-usage.md (<a href="https://redirect.github.com/actions/setup-python/issues/1094">#1094</a>)</li>
<li><a href="https://github.com/actions/setup-python/commit/18566f86b301499665bd3eb1a2247e0849c64fa5"><code>18566f8</code></a> Improve wording and &quot;fix example&quot; (remove 3.13) on testing against pre-releas...</li>
<li>Additional commits viewable in <a href="https://github.com/actions/setup-python/compare/v5.3.0...v6.2.0">compare view</a></li>
</ul>
</details>
<br />

Updates `actions/configure-pages` from 5 to 6
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/actions/configure-pages/releases">actions/configure-pages's releases</a>.</em></p>
<blockquote>
<h2>v6.0.0</h2>
<h1>Changelog</h1>
<ul>
<li>upgrade to node 24 <a href="https://github.com/salmanmkc"><code>@​salmanmkc</code></a> (<a href="https://redirect.github.com/actions/configure-pages/issues/186">#186</a>)</li>
<li>Upgrade IA Publish <a href="https://github.com/Jcambass"><code>@​Jcambass</code></a> (<a href="https://redirect.github.com/actions/configure-pages/issues/165">#165</a>)</li>
<li>Add workflow file for publishing releases to immutable action package <a href="https://github.com/Jcambass"><code>@​Jcambass</code></a> (<a href="https://redirect.github.com/actions/configure-pages/issues/163">#163</a>)</li>
<li>pin draft release version <a href="https://github.com/YiMysty"><code>@​YiMysty</code></a> (<a href="https://redirect.github.com/actions/configure-pages/issues/162">#162</a>)</li>
<li>Bump espree from 9.6.1 to 10.1.0 <a href="https://github.com/dependabot"><code>@​dependabot</code></a> (<a href="https://redirect.github.com/actions/configure-pages/issues/160">#160</a>)</li>
<li>Bump eslint-config-prettier from 8.8.0 to 9.1.0 <a href="https://github.com/dependabot"><code>@​dependabot</code></a> (<a href="https://redirect.github.com/actions/configure-pages/issues/143">#143</a>)</li>
<li>Be more friendly to Dependabot <a href="https://github.com/yoannchaudet"><code>@​yoannchaudet</code></a> (<a href="https://redirect.github.com/actions/configure-pages/issues/158">#158</a>)</li>
<li>Bump eslint-plugin-github from 4.10.2 to 5.0.1 <a href="https://github.com/dependabot"><code>@​dependabot</code></a> (<a href="https://redirect.github.com/actions/configure-pages/issues/154">#154</a>)</li>
<li>Bump braces from 3.0.2 to 3.0.3 in the npm_and_yarn group <a href="https://github.com/dependabot"><code>@​dependabot</code></a> (<a href="https://redirect.github.com/actions/configure-pages/issues/156">#156</a>)</li>
<li>Bump undici from 5.28.3 to 5.28.4 <a href="https://github.com/dependabot"><code>@​dependabot</code></a> (<a href="https://redirect.github.com/actions/configure-pages/issues/145">#145</a>)</li>
</ul>
<p>See details of <a href="https://github.com/actions/configure-pages/compare/v5.0.0...v5.0.1">all code changes</a> since previous release.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/actions/configure-pages/commit/45bfe0192ca1faeb007ade9deae92b16b8254a0d"><code>45bfe01</code></a> Merge pull request <a href="https://redirect.github.com/actions/configure-pages/issues/186">#186</a> from salmanmkc/node24</li>
<li><a href="https://github.com/actions/configure-pages/commit/d8770c2b3b71963902cec525cf516368b4411a78"><code>d8770c2</code></a> Update Node version from 20 to 24 in action.yml</li>
<li><a href="https://github.com/actions/configure-pages/commit/cb8a1a32801e6cdb7b111ce13761226bba88f67d"><code>cb8a1a3</code></a> upgrade to node 24</li>
<li><a href="https://github.com/actions/configure-pages/commit/d5606572c479bee637007364c6b4800ac4fc8573"><code>d560657</code></a> Merge pull request <a href="https://redirect.github.com/actions/configure-pages/issues/165">#165</a> from actions/Jcambass-patch-1</li>
<li><a href="https://github.com/actions/configure-pages/commit/35e0ac4e4038e070ce9da26f41143bc3cf3c7e1d"><code>35e0ac4</code></a> Upgrade IA Publish</li>
<li><a href="https://github.com/actions/configure-pages/commit/1dfbcbff6519463927204dc279c2e0d307824ee2"><code>1dfbcbf</code></a> Merge pull request <a href="https://redirect.github.com/actions/configure-pages/issues/163">#163</a> from actions/Jcambass-patch-1</li>
<li><a href="https://github.com/actions/configure-pages/commit/2f4f988792f75a5edcc39df0e1661f78999e0348"><code>2f4f988</code></a> Add workflow file for publishing releases to immutable action package</li>
<li><a href="https://github.com/actions/configure-pages/commit/0d7570ca8762e8c951911e8c9655d8973cc93174"><code>0d7570c</code></a> Merge pull request <a href="https://redirect.github.com/actions/configure-pages/issues/162">#162</a> from actions/pin-draft-release-verssion</li>
<li><a href="https://github.com/actions/configure-pages/commit/3ea19669a5cd11c46d23d6578d088b81fe8527e5"><code>3ea1966</code></a> pin draft release version</li>
<li><a href="https://github.com/actions/configure-pages/commit/aabcbc432d6b06d1fd5e8bf3cf756880c35e014d"><code>aabcbc4</code></a> Merge pull request <a href="https://redirect.github.com/actions/configure-pages/issues/160">#160</a> from actions/dependabot/npm_and_yarn/espree-10.1.0</li>
<li>Additional commits viewable in <a href="https://github.com/actions/configure-pages/compare/v5...v6">compare view</a></li>
</ul>
</details>
<br />

Updates `actions/upload-pages-artifact` from 3 to 5
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/actions/upload-pages-artifact/releases">actions/upload-pages-artifact's releases</a>.</em></p>
<blockquote>
<h2>v5.0.0</h2>
<h1>Changelog</h1>
<ul>
<li>Update upload-artifact action to version 7 <a href="https://github.com/Tom-van-Woudenberg"><code>@​Tom-van-Woudenberg</code></a> (<a href="https://redirect.github.com/actions/upload-pages-artifact/issues/139">#139</a>)</li>
<li>feat: add <code>include-hidden-files</code> input <a href="https://github.com/jonchurch"><code>@​jonchurch</code></a> (<a href="https://redirect.github.com/actions/upload-pages-artifact/issues/137">#137</a>)</li>
</ul>
<p>See details of <a href="https://github.com/actions/upload-pages-artifact/compare/v4.0.0...v4.0.1">all code changes</a> since previous release.</p>
<h2>v4.0.0</h2>
<h2>What's Changed</h2>
<ul>
<li>Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact by <a href="https://github.com/tsusdere"><code>@​tsusdere</code></a> in <a href="https://redirect.github.com/actions/upload-pages-artifact/pull/102">actions/upload-pages-artifact#102</a>
If you need to include dotfiles in your artifact: instead of using this action, create your own artifact according to these requirements <a href="https://github.com/actions/upload-pages-artifact?tab=readme-ov-file#artifact-validation">https://github.com/actions/upload-pages-artifact?tab=readme-ov-file#artifact-validation</a></li>
<li>Pin <code>actions/upload-artifact</code> to SHA by <a href="https://github.com/heavymachinery"><code>@​heavymachinery</code></a> in <a href="https://redirect.github.com/actions/upload-pages-artifact/pull/127">actions/upload-pages-artifact#127</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/actions/upload-pages-artifact/compare/v3.0.1...v4.0.0">https://github.com/actions/upload-pages-artifact/compare/v3.0.1...v4.0.0</a></p>
<h2>v3.0.1</h2>
<h1>Changelog</h1>
<ul>
<li>Group tar's output to prevent it from messing up action logs <a href="https://github.com/SilverRainZ"><code>@​SilverRainZ</code></a> (<a href="https://redirect.github.com/actions/upload-pages-artifact/issues/94">#94</a>)</li>
<li>Update README.md <a href="https://github.com/uiolee"><code>@​uiolee</code></a> (<a href="https://redirect.github.com/actions/upload-pages-artifact/issues/88">#88</a>)</li>
<li>Bump the non-breaking-changes group with 1 update <a href="https://github.com/dependabot"><code>@​dependabot</code></a> (<a href="https://redirect.github.com/actions/upload-pages-artifact/issues/92">#92</a>)</li>
<li>Update Dependabot config to group non-breaking changes <a href="https://github.com/JamesMGreene"><code>@​JamesMGreene</code></a> (<a href="https://redirect.github.com/actions/upload-pages-artifact/issues/91">#91</a>)</li>
<li>Bump actions/checkout from 3 to 4 <a href="https://github.com/dependabot"><code>@​dependabot</code></a> (<a href="https://redirect.github.com/actions/upload-pages-artifact/issues/76">#76</a>)</li>
</ul>
<p>See details of <a href="https://github.com/actions/upload-pages-artifact/compare/v3.0.0...v3.0.1">all code changes</a> since previous release.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/actions/upload-pages-artifact/commit/fc324d3547104276b827a68afc52ff2a11cc49c9"><code>fc324d3</code></a> Merge pull request <a href="https://redirect.github.com/actions/upload-pages-artifact/issues/139">#139</a> from Tom-van-Woudenberg/patch-1</li>
<li><a href="https://github.com/actions/upload-pages-artifact/commit/fe9d4b7d84090e1d8d9c53a0236f810d4e00d2c3"><code>fe9d4b7</code></a> Merge branch 'main' into patch-1</li>
<li><a href="https://github.com/actions/upload-pages-artifact/commit/0ca16172ca884f0a37117fed41734f29784cc980"><code>0ca1617</code></a> Merge pull request <a href="https://redirect.github.com/actions/upload-pages-artifact/issues/137">#137</a> from jonchurch/include-hidden-files</li>
<li><a href="https://github.com/actions/upload-pages-artifact/commit/57f0e8492b437b7818227931fef2faa1a379839b"><code>57f0e84</code></a> Update action.yml</li>
<li><a href="https://github.com/actions/upload-pages-artifact/commit/4a90348b2933470dc78cec55534259872a6d3c0d"><code>4a90348</code></a> v7 --&gt; hash</li>
<li><a href="https://github.com/actions/upload-pages-artifact/commit/56f665a6f297fa95f8d735b314187fb2d7764569"><code>56f665a</code></a> Update upload-artifact action to version 7</li>
<li><a href="https://github.com/actions/upload-pages-artifact/commit/f7615f5917213b24245d49ba96693d0f5375a414"><code>f7615f5</code></a> Add <code>include-hidden-files</code> input</li>
<li><a href="https://github.com/actions/upload-pages-artifact/commit/7b1f4a764d45c48632c6b24a0339c27f5614fb0b"><code>7b1f4a7</code></a> Merge pull request <a href="https://redirect.github.com/actions/upload-pages-artifact/issues/127">#127</a> from heavymachinery/pin-sha</li>
<li><a href="https://github.com/actions/upload-pages-artifact/commit/4cc19c7d3f3e6c87c68366501382a03c8b1ba6db"><code>4cc19c7</code></a> Pin <code>actions/upload-artifact</code> to SHA</li>
<li><a href="https://github.com/actions/upload-pages-artifact/commit/2d163be3ddce01512f3eea7ac5b7023b5d643ce1"><code>2d163be</code></a> Merge pull request <a href="https://redirect.github.com/actions/upload-pages-artifact/issues/107">#107</a> from KittyChiu/main</li>
<li>Additional commits viewable in <a href="https://github.com/actions/upload-pages-artifact/compare/v3...v5">compare view</a></li>
</ul>
</details>
<br />

Updates `actions/deploy-pages` from 4.1.5 to 5.0.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/actions/deploy-pages/releases">actions/deploy-pages's releases</a>.</em></p>
<blockquote>
<h2>v5.0.0</h2>
<h1>Changelog</h1>
<ul>
<li>Update Node.js version to 24.x <a href="https://github.com/salmanmkc"><code>@​salmanmkc</code></a> (<a href="https://redirect.github.com/actions/deploy-pages/issues/404">#404</a>)</li>
<li>Add workflow file for publishing releases to immutable action package <a href="https://github.com/Jcambass"><code>@​Jcambass</code></a> (<a href="https://redirect.github.com/actions/deploy-pages/issues/374">#374</a>)</li>
<li>Bump braces from 3.0.2 to 3.0.3 in the npm_and_yarn group across 1 directory <a href="https://github.com/dependabot"><code>@​dependabot</code></a> (<a href="https://redirect.github.com/actions/deploy-pages/issues/360">#360</a>)</li>
<li>Make the rebuild dist workflow work nicer with Dependabot <a href="https://github.com/yoannchaudet"><code>@​yoannchaudet</code></a> (<a href="https://redirect.github.com/actions/deploy-pages/issues/361">#361</a>)</li>
<li>Bump the non-breaking-changes group across 1 directory with 3 updates <a href="https://github.com/dependabot"><code>@​dependabot</code></a> (<a href="https://redirect.github.com/actions/deploy-pages/issues/358">#358</a>)</li>
<li>Delete repeated sentence <a href="https://github.com/garethsb"><code>@​garethsb</code></a> (<a href="https://redirect.github.com/actions/deploy-pages/issues/359">#359</a>)</li>
<li>Update README.md <a href="https://github.com/tsusdere"><code>@​tsusdere</code></a> (<a href="https://redirect.github.com/actions/deploy-pages/issues/348">#348</a>)</li>
<li>Bump the non-breaking-changes group with 4 updates <a href="https://github.com/dependabot"><code>@​dependabot</code></a> (<a href="https://redirect.github.com/actions/deploy-pages/issues/341">#341</a>)</li>
<li>Remove error message for file permissions <a href="https://github.com/TooManyBees"><code>@​TooManyBees</code></a> (<a href="https://redirect.github.com/actions/deploy-pages/issues/340">#340</a>)</li>
</ul>
<hr />
<p>See details of <a href="https://github.com/actions/deploy-pages/compare/v4.0.5...v4.0.6">all code changes</a> since previous release.</p>
<p>:warning: For use with products other than GitHub.com, such as GitHub Enterprise Server, please consult the <a href="https://github.com/actions/deploy-pages/#compatibility">compatibility table</a>.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li>See full diff in <a href="https://github.com/actions/deploy-pages/compare/v4.1.5...v5.0.0">compare view</a></li>
</ul>
</details>
<br />


## 评论

