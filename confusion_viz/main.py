import numpy as np
from sklearn.metrics import precision_recall_curve
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode


class ConfusionViz:
    
    
    def __init__(self):
        pass
    
    
    def fit(self, y_true, probas_pred, max_frames = 100):
        assert len(y_true) == len(probas_pred), 'y_true and probas_pred must have same length'
        assert set(y_true) == set([0, 1]), 'y_true values must be in {0, 1}'
        self.y_true = np.array(y_true)
        self.probas_pred = np.array(probas_pred)
        self.stats = self._get_stats(max_frames = max_frames)
        
        
    def _get_stats(self, max_frames):
        
        sample = len(self.y_true)
        positives = dict(zip(*np.unique(self.y_true, return_counts = True)))[1]
        
        precision, recall, threshold = precision_recall_curve(self.y_true, self.probas_pred)
        precision = np.append(np.append(positives / sample, precision[:-1]), 0)
        recall = np.append(1, recall)
        threshold = np.append(np.append(0, threshold), 1.1)
        select = np.round(np.linspace(0, len(threshold) - 1, min(max_frames, len(threshold)))).astype(int)
        precision, recall, threshold = [arr[select] for arr in [precision, recall, threshold]]
        
        predicted_positives = np.array([np.sum(self.probas_pred >= thres) for thres in threshold])
        true_positives = (precision * predicted_positives).astype(int)
        false_positives = predicted_positives - true_positives
        false_negatives = positives - true_positives
        true_negatives = len(self.y_true) - true_positives - false_positives - false_negatives
        
        stats = {
            'count': {
                'sample': sample,
                'positives': positives,
                'predicted positives': predicted_positives,
                'true positives': true_positives,
                'false positives': false_positives,
                'true negatives': true_negatives,
                'false negatives': false_negatives
            },
            'frac': {
                'precision': precision,
                'uplift': precision / precision[0],
                'recall': recall,
                'threshold': threshold,
                'positives': positives / sample,
                'predicted positives': predicted_positives / sample,
                'true positives': true_positives / sample,
                'false positives': false_positives / sample,
                'true negatives': true_negatives / sample,
                'false negatives': false_negatives / sample
            }

        }
        
        return stats
    
    
    def _index2coords(self, i):
                
        coords = {}
        
        coords['true negatives'] = [0, 1]
        coords['false negatives'] = [1 - self.stats['frac']['positives'] ** .5, 1]
        coords['true positives'] = [coords['false negatives'][0], coords['false negatives'][0] + self.stats['frac']['true positives'][i] ** .5]
        coords['false positives'] = [coords['true positives'][1] - self.stats['frac']['predicted positives'][i] ** .5, coords['true positives'][1]]
        coords['predicted positives'] = [.5] * 2
        coords['precision'] = [.5] * 2
        coords['uplift'] = [.5] * 2
        coords['recall'] = [.5] * 2

        return coords
    
    
    def _coord2Scatter(self, coord, **Scatter_kwargs):
        '''return a square given its coordinates'''
        
        coord_min = coord[0]
        coord_max = coord[1]
        
        Scatter = go.Scatter(
            x = [coord_min, coord_min, coord_max, coord_max, coord_min], 
            y = [coord_min, coord_max, coord_max, coord_min, coord_min],
            mode = 'lines',
            fill = 'toself',
            line_width = 0,
            **Scatter_kwargs
        )
        
        return Scatter
    
    
    def _index2Scatters(self, i):
        
        Scatters = {}
        
        coords = self._index2coords(i)
        
        Scatter_kwargs = {
            'true negatives': {
                'fillcolor': 'blue',
                'name': 'true negatives: {} ({} of sample)'.format(
                    '{:,}'.format(self.stats['count']['true negatives'][i]), 
                    '{:.2%}'.format(self.stats['frac']['true negatives'][i])
                )
            },
            'false negatives': {
                'fillcolor': 'yellow',
                'name': 'false negatives: {} ({} of sample)'.format(
                    '{:,}'.format(self.stats['count']['false negatives'][i]), 
                    '{:.2%}'.format(self.stats['frac']['false negatives'][i])
                )
            },
            'false positives': {
                'fillcolor': 'red',
                'name': 'false positives: {} ({} of sample)'.format(
                    '{:,}'.format(self.stats['count']['false positives'][i]), 
                    '{:.2%}'.format(self.stats['frac']['false positives'][i])
                )
            },
            'true positives': {
                'fillcolor': 'green',
                'name': 'true positives: {} ({} of sample)'.format(
                    '{:,}'.format(self.stats['count']['true positives'][i]), 
                    '{:.2%}'.format(self.stats['frac']['true positives'][i])              
                )
            },
            'predicted positives': {
                'opacity': 0, 
                'name': 'predicted positives: {} ({} of sample)'.format(
                    '{:,}'.format(self.stats['count']['predicted positives'][i]), 
                    '{:.2%}'.format(self.stats['frac']['predicted positives'][i])
                )
            },
            'precision': {
                'opacity': 0, 
                'name': 'precision: {:.2%}'.format(self.stats['frac']['precision'][i])
            },
            'uplift': {
                'opacity': 0, 
                'name': 'uplift: x{}'.format(round(self.stats['frac']['uplift'][i], 2))
            },
            'recall': {
                'opacity': 0, 
                'name': 'recall: {:.2%}'.format(self.stats['frac']['recall'][i])
            },
        }
        
        for key in coords.keys():
            Scatters[key] = self._coord2Scatter(coord = coords[key], **Scatter_kwargs[key])
            
        Scatters = [Scatters[key] for key in [
            'true negatives', 
            'false negatives', 
            'false positives', 
            'true positives', 
            'predicted positives', 
            'precision', 
            'uplift', 
            'recall'
        ]]
        
        return Scatters


    def _make_figure(self):
        
        frames, Scatters = [], []
        
        len_frames = len(self.stats['frac']['threshold'])
        len_Scatters_per_frame = len(self._index2Scatters(0))
        len_Scatters = len_frames * len_Scatters_per_frame
    
        for i in range(len_frames):
            Scatters.extend(self._index2Scatters(i))
            visible = [False] * i * len_Scatters_per_frame + [True] * len_Scatters_per_frame + [False] * (len_Scatters - (i + 1) * len_Scatters_per_frame)
            frames.append({
                'method': 'restyle',  
                'args': [{'visible': visible}],
                'label': 'P >= {:.2%}'.format(self.stats['frac']['threshold'][i])
            })

        layout = {
            'plot_bgcolor': 'white',
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'width': 900,
            'height': 600,
            'sliders': [{'steps': frames, 'x': 1.1, 'y': .05, 'yanchor': 'bottom'}],
            'legend': {'x': 1.1, 'y': .95}
        }

        self.Figure = go.Figure(data = Scatters, layout = layout)
        
        
    def show(self):
        
        init_notebook_mode()
        
        try:
            self.Figure.show()
            
        except:
            self._make_figure()
            self.Figure.show()
        
        
    def to_html(self, filepath):
        
        try:
            self.Figure.write_html(filepath)
            
        except:
            self._make_figure()
            self.Figure.write_html(filepath)
