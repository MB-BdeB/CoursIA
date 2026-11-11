import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, 10.5)
ax.set_ylim(0.4, 3.9)
ax.axis('off')

# Nodes (positions ajustées)
nodes = {
    'Clients': (1.0, 3.0),
    'Load Balancer': (3.2, 3.0),
    'API Servers': (5.4, 3.0),
    'Inference Cluster (GPUs)': (7.8, 3.0),
    'Storage (S3/NVMe)': (5.4, 1.25),
    'Monitoring': (9.2, 1.25)
}

box_w, box_h = 1.5, 0.62
for name, (x, y) in nodes.items():
    rect = patches.FancyBboxPatch(
        (x - box_w / 2, y - box_h / 2), box_w, box_h,
        boxstyle='round,pad=0.12', edgecolor='black', facecolor='#e8f6ff'
    )
    ax.add_patch(rect)
    ax.text(x, y, name, ha='center', va='center', fontsize=12)


def arrow(a, b, lw=1.5):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='->', lw=lw))


# Top horizontal flow arrows (placées au-dessus des boîtes)
top_y = 3.33
arrow((1.0 + box_w / 2, top_y), (3.2 - box_w / 2, top_y))
arrow((3.2 + box_w / 2, top_y), (5.4 - box_w / 2, top_y))
arrow((5.4 + box_w / 2, top_y), (7.8 - box_w / 2, top_y))

# Downstream arrows
arrow((5.4, 3.0 - box_h / 2), (5.4, 1.25 + box_h / 2))
arrow((7.8 + box_w / 2 - 0.05, 3.0), (9.2, 1.25), lw=1.7)
arrow((5.4 + box_w / 2, 1.25), (9.2 - box_w / 2, 1.25))

# Labels
ax.text(2.1, 3.52, 'HTTPS / gRPC', fontsize=10)
ax.text(6.2, 2.45, 'Batch requests / model calls', fontsize=10)

plt.savefig('c:/Users/Public/Documents/TELECHARGEMENT/BdeB/images/network_flow.png', dpi=170, bbox_inches='tight', pad_inches=0.2)
print('WROTE:c:/Users/Public/Documents/TELECHARGEMENT/BdeB/images/network_flow.png')
