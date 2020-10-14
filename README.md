# confusion_viz

Interactive visualization of the output of any binary classifier.

![](confusion_viz.gif)

The plot can be browsed in notebook mode, or downloaded as a html file.
**confusion_viz** can be installed in your local environment via:

<pre>
!pip install git+https://github.com/smazzanti/confusion_viz
</pre>

The package consists of one class called **ConfusionViz**.

<pre>
from confusion_viz import ConfusionViz
conf_viz = ConfusionViz()
conf_viz.fit(y_true, probas_pred)
conf_viz.show()    # shows plot in notebook mode
conf_viz.to_html('confusion_viz.html')    # stores plot as a html file
</pre>
