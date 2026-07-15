## dslr (data science: logistic regression)
42's logistic regression task (see also: [ft\_linear\_regression](https://github.com/DISN-kolo/ft_linear_regression))

### Objective
Given a dataset of various students in a fictional campus, calculate various metrics, display data in various ways, and build a student classifier based on their subject scores.

### Installing
0. you should have python3.13 or above (tested on 3.13)
1. for the first run, do `python -m venv venv`
2. both then and in every subsequent run, do `source venv/bin/activate`
3. if this is the first run, also do `pip install -r requirements.txt`
4. done working? `deactivate`

---

## Contents of the project
The project consists of multiple programs. See the sections below to find what you're after:
1. [Running visualizations](#running-visualizations)
2. [Predicting the data](#predicting-the-data)
3. [Additional exploration of prediction results](#additional-exploration-of-prediction-results)

---

### Running visualizations
For describing the data, use `./describe.py <datapath.csv>`.

You can build a histogram collection of subject scores by using `./histogram.py <datapath.csv>`.

You can build a pairwise collection of plots using `./pair_plot.py <datapath.csv>`. Note that the subjects have been hand-picked beforehand as the "most interesting" to look at based on the author's opinion.

### Predicting the data
To predict the students' houses, you have to train the model first.

Run `./logreg_train.py <datapath.csv> [<thetas.csv> <norms.csv> [.subjects]]`

The optionally specifiable `thetas.csv` and `norms.csv` filenames will contain the computed coefficients of the function that will get predicted and the normalization coefficients of the data, respectively. The default filenames are `thetas.csv` and `norms.csv`, respectively.

The optional `.subjects` file is used to specify which subjects to run training with. The format is as follows:

```
Subject Name as Seen in the Csv
Subject Name 2 as Seen in the Csv
<...>
Subject Name X as Seen in the Csv
```

*Note that you can only specify the subjects if you also choose to specify the custom `thetas` and `norms` files as well. Also note that you can only specify either both custom `thetas` and `norms` files at once, or neither.*

After you've successfully run the training script, you should have the resulting theta- and norms- containing files. To predict the students' houses, you must use them in the `logreg_predict` script. The syntax is as follows:

`./logreg_predict.py <datapath.csv> <thetas.csv> <norms.csv> [houses_output.csv [.subjects]]`

The optional `houses_output.csv` specifies the file to which the output of the prediction is written.

*Note that the thetas' and norms' paths are now obligatory for specification.*

*Note, per the subject's requirements, the index is being reset. To access the students by their original index, refer to a file that'll get generated as `<houses_output_filename>.original_index`.*

*Note that the `.subjects` file is only to be specified if the custom output is specified as well.*

### Additional exploration of prediction results

Say, you're operating with real data and have no answers for your test set upon which you've run the prediction algorithm. One of the methods of quickly checking the correctness of the results would be plotting the predicted data on top of the real data and visually estimating if it compares well.

You can do that using the aforementioned `pair_plot` script:

`./pair_plot.py <datapath_training.csv> <datapath_test.csv> <predictions.original_index>`

*Note that you will have to use the original-index-containing prediction results, produced by the `logreg_predict` script.*

This will plot the data on top of the scatter plots of the true data, using `x` crosses as data points to differentiate from the default circles of the surely-known data.

---

### Licensing

- [LICENSES/LICENSE-MIT](LICENSES/LICENSE-MIT)
