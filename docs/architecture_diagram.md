# Architecture Diagram Draft

This diagram shows the planned flow of the Credit Growth Analytics Pipeline.

```mermaid
flowchart TD

    A["Synthetic Financial Services Data"] --> A1["customers.csv"]
    A --> A2["monthly_behaviour.csv"]
    A --> A3["credit_products.csv"]
    A --> A4["credit_outcomes.csv"]
    A --> A5["treatment_log_sample.csv"]

    A1 --> B["Data Preparation and Quality Checks"]
    A2 --> B
    A3 --> B
    A4 --> B

    B --> C["Feature Engineering Layer"]
    C --> C1["Customer tenure and demographics"]
    C --> C2["Savings and balance behaviour"]
    C --> C3["Credit exposure and product depth"]
    C --> C4["Engagement and campaign history"]

    C --> D1["Conversion Model"]
    C --> D2["Responsible Behaviour Model"]
    A3 --> D3["Expected Value Calculation"]

    D1 --> E["Responsible NBA Score"]
    D2 --> E
    D3 --> E

    E --> F["Eligibility and Governance Filters"]
    F --> F1["Affordability / exposure checks"]
    F --> F2["High-risk exclusion"]
    F --> F3["Recent contact exclusion"]
    F --> F4["Data quality flags"]

    F --> G["Next-Best-Action Ranking"]
    G --> H["Advisor-Ready Recommendation List"]

    H --> I["Visualisation Layer"]
    I --> I1["Executive Overview"]
    I --> I2["Customer Ranking"]
    I --> I3["Model Performance"]
    I --> I4["Governance Monitoring"]

    H --> J["Treatment Log Feedback Loop"]
    J --> K["Future model monitoring and learning"]
    K --> C
```

## Interpretation

The project is designed as a closed-loop analytics product:

1. synthetic data is generated safely;
2. customer-month features are engineered;
3. conversion, responsible behaviour, and expected value are estimated;
4. customers are ranked using a responsible Next-Best-Action score;
5. governance filters protect against unsuitable targeting;
6. the dashboard translates model outputs into business decisions;
7. the treatment log enables future learning from interventions.
