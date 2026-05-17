# v1.0.0 Release Checklist

This checklist documents the final manual GitHub settings recommended for the public portfolio release.

## 1. Repository topics

Add the following topics from the GitHub repository main page:

```text
machine-learning
data-science
customer-analytics
credit-risk
financial-services
next-best-action
streamlit
scikit-learn
python
business-intelligence
responsible-ai
portfolio-project
```

Path in GitHub:

```text
Repository main page -> About section -> gear icon -> Topics
```

## 2. Social preview image

Use the main dashboard screenshot as the social preview image.

Recommended file:

```text
docs/assets/screenshots/01_dashboard_landing.png
```

Path in GitHub:

```text
Repository -> Settings -> General -> Social preview
```

## 3. GitHub release

Create a release called:

```text
v1.0.0
```

Suggested release title:

```text
v1.0.0 - Public portfolio release
```

Suggested release notes:

```markdown
## v1.0.0 - Public portfolio release

This release marks the first public portfolio version of the Credit Growth Analytics Pipeline.

### Included

- Reproducible Python pipeline for responsible credit-growth Next-Best-Action analytics
- Synthetic financial-services data generation
- Conversion and responsible credit-behaviour models
- Expected-value scoring and advisor-ready customer ranking
- Streamlit dashboard with executive, ranking, model-performance and governance pages
- Dashboard screenshots embedded in the README
- GitHub Actions validation workflow
- MIT licence
- Project disclaimer
- Changelog
- Citation metadata
- Makefile command shortcuts

### Notes

- All data is synthetic.
- This project is for portfolio demonstration and decision-support design.
- It is not an automated credit approval system or real credit policy.
```

Path in GitHub:

```text
Repository main page -> Releases -> Draft a new release
```

Recommended tag:

```text
v1.0.0
```

Target branch:

```text
main
```

## 4. Final validation

After creating the release, confirm that:

1. the README displays the live GitHub Actions badge;
2. the latest Actions run is green;
3. dashboard screenshots render in the README;
4. the repository has a visible MIT licence;
5. the repository topics are visible under the About section;
6. the social preview image appears when the repository link is shared.
