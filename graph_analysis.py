
import csv
import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# 1. Load the 5000-account dataset
with open("accounts.csv", "r", encoding="utf-8-sig") as file:
    rows = list(csv.DictReader(file))

print("DATASET LOADED SUCCESSFULLY!")
print("Total accounts:", len(rows))

# 2. Select profile features (do not use fake label)
features = [
    "profile pic",
    "nums/length username",
    "fullname words",
    "nums/length fullname",
    "name==username",
    "description length",
    "external URL",
    "private",
    "#posts",
    "#followers",
    "#follows"
]

# 3. Convert feature values into numbers
data = []

for row in rows:
    values = []
    for feature in features:
        value = float(row[feature])
        if feature in ["#posts", "#followers", "#follows"]:
            value = math.log1p(max(0, value))
        values.append(value)
    data.append(values)

X = np.array(data)

# 4. Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Find the 5 nearest similar accounts
neighbors = NearestNeighbors(
    n_neighbors=6,
    metric="cosine"
)
neighbors.fit(X_scaled)

distances, indices = neighbors.kneighbors(X_scaled)

# 6. Create the relationship network
G = nx.Graph()

for i in range(len(rows)):
    G.add_node(
        f"account_{i + 1}",
        label=rows[i]["fake"]
    )

for i in range(len(rows)):
    for distance, neighbor in zip(distances[i][1:], indices[i][1:]):
        similarity = 1 - distance

        if similarity >= 0.90:
            G.add_edge(
                f"account_{i + 1}",
                f"account_{neighbor + 1}",
                similarity=round(float(similarity), 4)
            )

# 7. Find connected groups
groups = [
    component for component in nx.connected_components(G)
    if len(component) >= 2
]

# 8. Save network files
nx.write_graphml(G, "account_relationships.graphml")

with open("graph_edges.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["account_1", "account_2", "similarity"])

    for a, b, details in G.edges(data=True):
        writer.writerow([a, b, details["similarity"]])

with open("coordinated_groups.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["group_id", "account_id", "fake_label"])

    for group_id, group in enumerate(groups, start=1):
        for account in sorted(group):
            writer.writerow([
                group_id,
                account,
                G.nodes[account]["label"]
            ])

# 9. Display results
print("\nNETWORK ANALYSIS COMPLETED!")
print("Total accounts:", G.number_of_nodes())
print("Total connections:", G.number_of_edges())
print("Potential similarity groups:", len(groups))

for group_id, group in enumerate(groups, start=1):
    print(f"Group {group_id}: {len(group)} accounts")

# 10. Draw and save the network graph
if G.number_of_edges() > 0:
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G, pos,
        node_size=15,
        with_labels=False,
        edge_color="gray"
    )
    plt.title("Instagram Account Similarity Network")
    plt.savefig("relationship_graph.png", dpi=200)
    plt.close()
    print("Graph image saved: relationship_graph.png")
else:
    print("No connections met the similarity threshold.")

print("\nFiles saved successfully!")
