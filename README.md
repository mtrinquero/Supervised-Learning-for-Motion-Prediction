# Supervised Learning for Motion Prediction

## AI for robotics masters coursework - Ga Tech - Supervised Learning for Motion Prediction
## Summary of Approaches Used:
1. K-Nearest Neighbors (KNN) with enriched velocity and heading, single point prediction – This approach provided the best error rate however when looking at the visual plots the predicted and actual path often diverge quickly. We expected this as the error noise is increasing and each prediction is less certain than the previous.
2. Extremely Randomized Trees (Extra Trees) with enriched velocity and heading, single point prediction – this approach provided worse results on the test data, more investigation is required to explain the discrepancy
3. Both of the above with additional enriched data – as mentioned before, adding sliding averages for heading and velocity surprisingly did not improve either algorithm’s results.
4. Extra Trees and KNN predicting the next 60 based on a sliding window of size k, where k values of sizes 5, 10, 20, 30, and 60. Tested with and without enriched data.
