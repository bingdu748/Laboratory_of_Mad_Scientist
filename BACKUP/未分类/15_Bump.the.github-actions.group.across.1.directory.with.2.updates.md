# [Bump the github-actions group across 1 directory with 2 updates](https://github.com/bingdu748/Laboratory_of_Mad_Scientist/pull/15)

## 元信息

- 创建时间: 2026-06-10 03:28:51
- 更新时间: 2026-06-10 05:16:08

## 内容

Bumps the github-actions group with 2 updates in the / directory: [actions/checkout](https://github.com/actions/checkout) and [actions/upload-pages-artifact](https://github.com/actions/upload-pages-artifact).

Updates `actions/checkout` from 5 to 6
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/actions/checkout/releases">actions/checkout's releases</a>.</em></p>
<blockquote>
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
<p><strong>Full Changelog</strong>: <a href="https://github.com/actions/checkout/compare/v5...v5.0.1">https://github.com/actions/checkout/compare/v5...v5.0.1</a></p>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/actions/checkout/blob/main/CHANGELOG.md">actions/checkout's changelog</a>.</em></p>
<blockquote>
<h1>Changelog</h1>
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
<h2>v4.2.2</h2>
<ul>
<li><code>url-helper.ts</code> now leverages well-known environment variables by <a href="https://github.com/jww3"><code>@​jww3</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/1941">actions/checkout#1941</a></li>
<li>Expand unit test coverage for <code>isGhes</code> by <a href="https://github.com/jww3"><code>@​jww3</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/1946">actions/checkout#1946</a></li>
</ul>
<h2>v4.2.1</h2>
<ul>
<li>Check out other refs/* by commit if provided, fall back to ref by <a href="https://github.com/orhantoy"><code>@​orhantoy</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/1924">actions/checkout#1924</a></li>
</ul>
<h2>v4.2.0</h2>
<ul>
<li>Add Ref and Commit outputs by <a href="https://github.com/lucacome"><code>@​lucacome</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/1180">actions/checkout#1180</a></li>
<li>Dependency updates by <a href="https://github.com/dependabot"><code>@​dependabot</code></a>- <a href="https://redirect.github.com/actions/checkout/pull/1777">actions/checkout#1777</a>, <a href="https://redirect.github.com/actions/checkout/pull/1872">actions/checkout#1872</a></li>
</ul>
<h2>v4.1.7</h2>
<ul>
<li>Bump the minor-npm-dependencies group across 1 directory with 4 updates by <a href="https://github.com/dependabot"><code>@​dependabot</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/1739">actions/checkout#1739</a></li>
<li>Bump actions/checkout from 3 to 4 by <a href="https://github.com/dependabot"><code>@​dependabot</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/1697">actions/checkout#1697</a></li>
<li>Check out other refs/* by commit by <a href="https://github.com/orhantoy"><code>@​orhantoy</code></a> in <a href="https://redirect.github.com/actions/checkout/pull/1774">actions/checkout#1774</a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
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
<li>Additional commits viewable in <a href="https://github.com/actions/checkout/compare/v5...v6">compare view</a></li>
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


## 评论

