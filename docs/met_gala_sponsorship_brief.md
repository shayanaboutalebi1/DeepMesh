# DeepMesh - Met Gala Sponsorship Automation

**Use Case**: Modeling who actually paid for high-profile access (e.g. Kim Kardashian’s Met Gala ticket).

### Key Insight
- Met Gala is **invitation-only**.
- Tickets: ~$100,000 each | Tables: ~$350,000.
- Most celebrities (including Kim Kardashian) do **not** pay personally.
- Luxury brands/designers buy tables and extend invitations.

### DeepMesh Implementation

- **Nodes**: Sponsor (brand), Guest (celebrity/influencer), Gatekeeper
- **Path Types**:
  - `sponsored` → Highest priority (brand pays)
  - `invited` → Medium
  - `paid` → Direct payment
  - `self_funded` → Lowest

**Scoring Formula**:  
`(Reach × Influence) / (Risk + Cost Factor)`

**Output**: Ranked decision graph showing best sponsored routes.

### How to Use
```python
from modules.sponsorship_mesh import MetGalaSponsorshipMesh

mesh = MetGalaSponsorshipMesh()
mesh.map_sponsored_path("BrandName", "TargetPerson", projected_reach=12000000, risk=0.18)
print(mesh.rank_paths())
```

This module works independently and does **not** affect existing DeepMesh functionality.
