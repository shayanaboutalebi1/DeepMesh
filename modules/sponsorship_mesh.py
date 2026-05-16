# modules/sponsorship_mesh.py
"""
DeepMesh - Met Gala Sponsorship & Invited Access Module
Analogy: Kim Kardashian’s Met Gala ticket was paid by a luxury brand/designer (table sponsor),
not personally by her. This module models sponsored, invited, and paid paths.
"""

class SponsorshipNode:
    def __init__(self, name: str, node_type: str = "participant", value: float = 0.0, 
                 reach: int = 0, influence: float = 0.0, risk: float = 0.0):
        self.name = name
        self.node_type = node_type          # sponsor, guest, gatekeeper, hybrid
        self.value = value
        self.reach = reach
        self.influence = influence
        self.risk = risk
        self.paths = []

    def add_path(self, target: str, path_type: str = "sponsored", score: float = 0.0):
        self.paths.append({
            "target": target,
            "type": path_type,   # sponsored, invited, paid, self_funded
            "score": score
        })

class MetGalaSponsorshipMesh:
    def __init__(self):
        self.nodes = {}
        self.gatekeeper = "Gatekeeper"   # e.g. Anna Wintour equivalent

    def add_node(self, node: SponsorshipNode):
        self.nodes[node.name] = node

    def map_sponsored_path(self, sponsor: str, guest: str, projected_reach: int, risk: float = 0.2):
        """Create a sponsored path (Brand pays → Guest gets access)"""
        if sponsor not in self.nodes:
            self.add_node(SponsorshipNode(sponsor, "sponsor", reach=projected_reach))
        if guest not in self.nodes:
            self.add_node(SponsorshipNode(guest, "guest", influence=8.5))

        # Higher score = better reach-to-risk ratio
        score = (projected_reach * 0.75) / (risk + 0.1)
        
        self.nodes[sponsor].add_path(guest, "sponsored", score)
        print(f"[DeepMesh] ✓ Sponsored path created: {sponsor} → {guest} | Score: {score:.3f}")

    def rank_paths(self):
        ranked = []
        for node_name, node in self.nodes.items():
            for path in node.paths:
                ranked.append({
                    "from": node_name,
                    "to": path["target"],
                    "type": path["type"],
                    "score": path["score"]
                })
        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked

# Quick test
if __name__ == "__main__":
    mesh = MetGalaSponsorshipMesh()
    mesh.map_sponsored_path("LouisVuitton", "KimKardashian", projected_reach=8500000, risk=0.15)
    print("\nRanked Paths:")
    for path in mesh.rank_paths():
        print(path)
