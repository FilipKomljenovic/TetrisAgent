from joblib import Parallel, delayed

from evaluator import Evaluator

N_JOBS = 8


def work(id):
    evaluator = Evaluator(id)
    return evaluator.evaluate()


ids = range(0, N_JOBS)
results = Parallel(n_jobs=N_JOBS, verbose=0, backend="multiprocessing")(map(delayed(work), ids))
best = 0
index = 0

for i, res in results:
    if res[0] > best:
        best = res[0]
        index = i

print("\n")
print("Best agent score:", results[index][0], "\nWeights:", results[index][1])
