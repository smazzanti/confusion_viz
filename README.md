# confusion_viz

Interactive visualization of the output of any binary classifier.

![](confusion_viz.gif)

## Reference

[Towards Data Science: Interactive visualization of the output of any binary classifier - in 5 Lines of Python](https://towardsdatascience.com/interactive-visualization-of-binary-classification-in-5-lines-of-python-9c1f627ded8)

## How to install

**confusion_viz** can be installed in your local environment via:

<pre>
!pip install git+https://github.com/smazzanti/confusion_viz
</pre>

## How to use

The package consists of one class called **ConfusionViz**.
Here is a snippet containing basically everything you need to know:

<pre>
from confusion_viz import ConfusionViz
conf_viz = ConfusionViz()
conf_viz.fit(y_true, probas_pred)
conf_viz.show()    # shows plot in notebook mode
conf_viz.to_html('confusion_viz.html')    # stores plot as a html file
</pre>
