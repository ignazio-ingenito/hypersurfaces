import json
import datetime

from webapp.db import session
from webapp.models import Dataset, AudioFile, Peak, RootMeanSquare


class Seed(object):
    """ Utility class to seed the date for the initial setup """

    @staticmethod
    def run():
        # load data from json file

        data = Seed.load_from_json('data.json')

        # seed the dataset table
        Seed.seed_dataset(data)

    @staticmethod
    def load_from_json(filename):
        """Load file from json file all data to seed the db"""

        with open(filename, 'r') as file:
            return json.load(file)

    @staticmethod
    def seed_dataset(data):
        """Seed the Dataset table"""

        timestamp = datetime.datetime.now()

        try:
            # set values
            dataset = Dataset()
            dataset.name = f'Dataset {timestamp.utcnow()}'
            dataset.description = f'Dataset created on {timestamp}'
            dataset.date_created = timestamp
            session.add(dataset)
            session.commit()
            print(f'Dataset {dataset.id} inserted')

            # seed the audiofile table
            Seed.seed_audio_file(dataset.id, data)
        except Exception as e:
            print(f'seed_dataset: {e}')

    @staticmethod
    def seed_audio_file(dataset_id, data):
        """Seed the Audiofile table"""

        for item in data:
            try:
                audiofile = AudioFile()
                audiofile.id_dataset = dataset_id
                audiofile.audio_path = item['file']
                audiofile.date_created = datetime.datetime.now()
                session.add(audiofile)
                session.commit()
                print(f'AudioFile: {audiofile.id} inserted')

                # get the data relative to the currenr audiofile
                items = [d for d in data if d['file'] == item['file']][0]

                # seed the peak table
                Seed.seed_peak(audiofile.id, items)

                # seed the rms table
                Seed.seed_rms(audiofile.id, items)

            except Exception as e:
                print(f'seed_audio_file: {e}')

    @staticmethod
    def seed_peak(audiofile_id, data):
        """ seed the peak table """

        count = 0
        for item in data['peaks']:
            try:
                peak = Peak()
                peak.id_audiofile = audiofile_id
                peak.peak = item
                session.add(peak)
                session.commit()
                count += 1
            except Exception as e:
                print(f'seed_peak: {e}')

        print(f'Peak: {count} rows inserted')

    @staticmethod
    def seed_rms(audiofile_id, data):
        """ Seed the rms table """

        count = 0
        for item in data['rms']:
            try:
                rms = RootMeanSquare()
                rms.time = item['time']
                rms.value = item['value']
                rms.id_audiofile = audiofile_id
                session.add(rms)
                session.commit()
                count += 1
            except Exception as e:
                print(f'seed_rms: {e}')

        print(f'RootMeanSquare: {count} rows inserted')