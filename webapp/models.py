"""Database file."""

from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship

from webapp.db import Base, engine


class Dataset(Base):
    """Dataset table."""

    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))
    description = Column(String(512))
    date_created = Column(DateTime())

    # relationships
    audiofile = relationship("AudioFile", back_populates='dataset')


class AudioFile(Base):
    """Dataset table."""

    __tablename__ = 'audio_file'
    id = Column(Integer, primary_key=True, autoincrement=True)
    audio_path = Column(String(256))
    date_created = Column(DateTime())
    id_dataset = Column(Integer, ForeignKey('dataset.id', ondelete='cascade'))

    # relationships
    dataset = relationship("Dataset", back_populates='audiofile')
    peaks = relationship("Peak", back_populates='audiofile')
    rms = relationship("RootMeanSquare", back_populates='audiofile')


class Peak(Base):
    """Peaks table"""

    __tablename__ = 'peaks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    peak = Column(DECIMAL(40, 20))
    id_audiofile = Column(Integer, ForeignKey(AudioFile.id, ondelete='cascade'))

    # relationships
    audiofile = relationship('AudioFile', back_populates='peaks')
    rms = relationship('RootMeanSquare', back_populates='peaks')


class RootMeanSquare(Base):
    """Root Mean Square"""

    __tablename__ = 'rms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DECIMAL(40, 20))
    value = Column(DECIMAL(40, 20))
    id_audiofile = Column(Integer, ForeignKey(AudioFile.id, ondelete='cascade'))
    id_peak = Column(Integer, ForeignKey(Peak.id, ondelete='cascade'))

    # relationships
    audiofile = relationship('AudioFile', back_populates='rms')
    peaks = relationship('Peak', back_populates='rms')


def init_db():
    """Import all modules here that might define models.

    # so that they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    """
    Base.metadata.create_all(bind=engine)
