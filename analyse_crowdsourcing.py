import csv
import matplotlib.pyplot as plt

EMOTIONS = [
    'excitement',
    'happy',
    'pleasant',
    'surprise',
    'fear',
    'angry',
]

result = {e: {'total': 0, 'correct': 0} for e in EMOTIONS}

with open('cf_report_1556720_full.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        result[row['emotion']]['total'] += 1
        if row['emotion'] == row['result']:
            # correct
            result[row['emotion']]['correct'] += 1

plt.style.use("bmh")
plt.rcParams["figure.figsize"] = (15, 5)
plt.bar(result.keys(), [v['correct'] / v['total'] for k, v in result.items()])
plt.xlabel('emotion')
plt.ylabel('accuracy')
plt.savefig("accuracy.pdf", bbox_inches='tight')
plt.show()
