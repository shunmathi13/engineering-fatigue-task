# Validation

## Environment

- Docker image: `engineering-fatigue`
- Python: 3.12
- NumPy: 1.26.4
- SciPy: 1.13.1
- pandas: 2.2.2

## Validation Commands

### Build

```bash
docker build -f environment/Dockerfile -t engineering-fatigue .
```

### Run solution

```bash
docker run --rm -v "$(pwd)/environment/data:/root/data" -v "$(pwd)/solution:/root/solution" -v "$(pwd)/results:/root/results" engineering-fatigue python /root/solution/solve.py
```

### Run tests

```bash
docker run --rm -v "$(pwd)/environment/data:/root/data" -v "$(pwd)/results:/root/results" -v "$(pwd)/tests:/root/tests" engineering-fatigue python /root/tests/test_fatigue.py
```

## Validation Result

The Docker image built successfully.

The solution executed successfully and produced:

- `results/fatigue_analysis.csv`
- `results/engineering_report.md`

The validation test script completed successfully with no assertion failures.

The computed critical loading block was **Block 4**.
