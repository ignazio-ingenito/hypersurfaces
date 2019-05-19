import io
import os
import base64
from itertools import groupby

import scipy.io.wavfile
import matplotlib.pyplot as plt
import numpy as np

from webapp.db import session
from webapp.models import AudioFile, Peak


class Plot(object):
    """Utility class to generate plot"""

    @staticmethod
    def get_files():
        """ get the list of wav file from the db """
        rows = session.query(AudioFile.audio_path).all()
        files = [os.path.basename(file.audio_path) for file in rows]
        return files

    @staticmethod
    def get_dataset():
        """ Create the dataset to to render the page """
        files = Plot.get_files()

        dataset = []
        for file in files:
            html, has_peaks = Plot.get_plot_image(file)
            dataset.append({
                "file": file,
                "html": html,
                "has_peaks": has_peaks
            })
        return dataset

    @staticmethod
    def get_plot_image(file):
        """ Create the plot image """

        has_peaks = False
        img = io.BytesIO()

        try:
            # Load the data and calculate the time of each sample
            rate, data = scipy.io.wavfile.read(file)
            times = np.arange(len(data)) / float(rate)

            # Make the plot
            plt.fill_between(times, data)
            plt.xlim(times[0], times[-1])
            plt.xlabel('time (sec)')
            plt.ylabel('amplitude')

            # Get the list of peaks
            peaks = Plot.get_peaks(file)

            # Make the plot
            if peaks:
                has_peaks = True
                axes = plt.gca()
                ymin, ymax = axes.get_ylim()
                for peak in peaks:
                    plt.plot(peak, [ymin, ymax], linewidth=0.5, antialiased=True, color='orange')

            # create the base64 png/image string
            plt.savefig(img, format='png')
            img.seek(0)
            bytes = img.getvalue()
            img64 = base64.b64encode(bytes).decode('utf-8')
            img.close()
            plt.close()

            return f'data:image/png;base64, {img64}', has_peaks
        except ValueError as e:
            return f'Invalid file', has_peaks
        except Exception as e:
            return str(e), has_peaks

    @staticmethod
    def get_peaks(filename):
        """ Retrive all the peaks value from the db """
        rows = session.query(Peak.peak) \
                      .join(AudioFile, AudioFile.id == Peak.id_audiofile) \
                      .filter(AudioFile.audio_path.like(f'%{filename}'))\
                      .order_by(Peak.peak) \
                      .all()

        peaks = []
        for key, g in groupby(rows):
            group = list(g)
            peaks.append(group[0:2])

        return peaks
