# Winning Space Race with Data Science

This is the capstone project I had to develop in order to get approved in the IBM Data Science Professional Certificate.

![certificate](https://github.com/tina-ds/Applied-Data-Science-Capstone/blob/e7ff4ba20e8909ae96b110e97fbe8cb2fd8c4fbe/images/certificate.png)
In this work, I will predict whether the first stage of the Falcon 9 will land successfully. SpaceX advertises $62 million cost of Falcon 9 rocket launches on its website; other providers cost more than $165 million each, most of the savings is because Space X being able to reuse the first stage.

Therefore, if I can determine whether the first stage successfully lands, this information could be used if an alternative company wants to bid against SpaceX for a rocket launch.

The goal of this project is to create a machine learning pipeline to predict whether the landing of the first stage will be successful and what factors influence it.

## Problems I want to find answers

- Factors that determine successful rocket landing.

- The effect of each relationship of rocket variables on outcome.

- Conditions which will aid SpaceX have to achieve the best results.
## Executive Summary
  1. Data Collection through API
  2. Data Collection with Web Scraping
  3. Data Wrangling
  4. Exploratory Data Analysis with Data Visualization with Folium and a Dashboard
  5. Exploratory Data Analysis with SQL
  6. Predictive Analysis (Logistic Regression, SVM, Decision Tree and KNN)
  7. Exploratory data analysis results
  8. Interactive analytics demo in screenshots
  9. Predictive analysis results
## Conclusions
  - The greater the number of launches (more than 40), the higher the success rate for the rocket.
  - We see that the success rates for a weighted average payload (1952kg - 5300kg) are higher than for a very light payload (<1952kg) or a heavier payload (>5300kg).
  - ES-L1, GEO, HEO, SSO orbits have the highest success rates.
  - In LEO orbit, success appears as a function of the number of launches; on the other hand, there seems to be no connection between the GTO flight number.
  - With heavy payloads, landing success or positive landing speed is greater for Polar, LEO and ISS orbits.
  - In addition, the proximity of the equator line, coastline, highways has a positive effect on the probability of a successful rocket launch.
  - SpaceX launch success rates are relatively increasing over time, and it looks like they will hit the required target soon.












