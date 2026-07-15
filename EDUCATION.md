## Maths and such
This project uses some stats, maths and all that good stuff. Here are some explanations of the things used.

---

### Table of contents

0. [Describing the data](#describing-the-data)
1. [Datavis: Histogram](#datavis-histogram)
2. [Datavis: Scatter plot](#datavis-scatter-plot)
3. [Datavis: Pair plot](#datavis-pair-plot)
4. [Logistic regression: Training](#logistic-regression-training)
5. [Logistic regression: Prediction](#logistic-regression-prediction)

---

### Describing the data

The `describe.py` program performs a series of basic stats operations used to describe a dataset: count, mean, std, min/max, various percentiles.

The insightful part of this subtask (if one could call it that) was realizing there are missing fields in the original dataset. This prompted the creation of "anti-nan" tools. In fact, these tools already exist in pandas and other libraries, but the point of this exercise was to re-create the basics manually.

### Datavis: Histogram

The `histogram.py` program plots histograms of subject scores, giving each house a unique visual theme in the process.

The main point of this graph is a nice visual representation of quantities of datapoints along percentile buckets (i.e., it counts the amount of points that fit between X and X+n percents of the score range, for every division-by-n of the range)

To answer the question provided in this section of the subject - *Which Hogwarts course has a homogeneous score distribution between all four houses?* - "Arithmancy" and "Care of Magical Creatures" look particularly useless for distinguishing between the houses.

### Datavis: Scatter plot

The `scatter_plot.py` program plots scatter plots of all the unique 2-dimentional combinations of subject scores.

The main point of this graph is to check for potential dimentions which would help differentiate beween houses.

The subject's got a question here that asks for two features that are similar, and the answer is definitely "Astronomy" and "Defense Against the Dark Arts". Worth noting, "History of Magic" and "Flying" are quite close as well.

### Datavis: Pair plot

The `pair_plot.py` program plots scatter plots and histograms of all the possible combinations of a selected range of subjects. The subjects were selected manually after looking at what the histograms had to offer.

The question presented: "From this visualization, which features are you going to use for your logistic regression?"

My answer: "Ancient Runes", "Divination" and "Astronomy" seem to go pretty well together.

### Logistic regression: Training

Alright, we've arrived at something much more interesting.

In this part, we train our prediction model. We do it based on the assumption that subject scores can be put in a function which would result in a 0 or 1 answer for whether or not a person with said scores belongs to a chosen house. Thus, for every house we need to do separate training sessions. Okay, and what does each session contain? 

### Logistic regression: Prediction
