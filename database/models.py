from app import db
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BOOLEAN, FLOAT
from sqlalchemy.orm import relationship

# euclid db models: __repr__(self) tells python what the object/class
#                   should be printed as
#
# SQLAlchemy automatically sets the first Integer primary key (not marked as a
# foreign key) with AUTO_INCREMENT = TRUE
#
# GEO2Enrichr Classes (Tables) in euclid db (MySQL)
#
# Extractions table only has id. Represents one instance of the
# user submitting a GEO2Enrichr extraction


class Extractions(db.Model):
    __tablename__ = 'Extractions'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    ExtractionsToGeneLists = relationship('ExtractionsToGeneLists',
                                          backref='Extractions',
                                          post_update=True)
    ExtractionsToCells = relationship('ExtractionsToCells',
                                      backref='Extractions',
                                      post_update=True)
    ExtractionsToDEMSs = relationship('ExtractionsToDEMs',
                                      backref='Extractions',
                                      post_update=True)
    ExtractionsToSamples = relationship('ExtractionsToSamples',
                                        backref='Extractions',
                                        post_update=True)
    ExtractionsToPerturbations = relationship('ExtractionsToPerturbations',
                                              backref='Extractions',
                                              post_update=True)
    ExtractionsToDatasets = relationship('ExtractionsToDatasets',
                                         backref='Extractions',
                                         post_update=True)

    def __repr__(self):
        return '<Extractions %r>' % (self.id)

# Extractions to Datasets to Samples/Platforms/Organisms/Datatypes/Diseases


class ExtractionsToDatasets(db.Model):
    __tablename__ = 'ExtractionsToDatasets'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    ExtractionId = db.Column(INTEGER(unsigned=True),
                             db.ForeignKey(
                                 'Extractions.id',
                                 ondelete='CASCADE'))
    DatasetId = db.Column(INTEGER(unsigned=True),
                          db.ForeignKey('Datasets.id',
                                        ondelete='CASCADE'))
    Datasets = relationship('Datasets',
                            backref='ExtractionsToDatasets',
                            post_update=True)

    def __repr__(self):
        return '<ExtractionsToDataSets %r>' % (self.id)


class ExtractionsToSamples(db.Model):
    __tablename__ = 'ExtractionsToSamples'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    ExtractionId = db.Column(INTEGER(unsigned=True),
                             db.ForeignKey(
                                 'Extractions.id',
                                 ondelete='CASCADE'))
    SampleId = db.Column(INTEGER(unsigned=True),
                         db.ForeignKey('Samples.id',
                                       ondelete='CASCADE'))
    Samples = relationship('Samples',
                           backref='ExtractionsToSamples',
                           post_update=True)

    def __repr__(self):
        return '<ExtractionsToSamples %r>' % (self.id)


class Datasets(db.Model):
    __tablename__ = 'Datasets'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    Accession = db.Column(VARCHAR(20), unique=True, nullable=False)
    GeoLink = db.Column(VARCHAR(75))
    Title = db.Column(VARCHAR(255))
    ProcessedBool = db.Column(db.BOOLEAN)
    DatasetsToSamples = relationship('DatasetsToSamples',
                                     backref='Datasets',
                                     post_update=True)
    DatasetsToPlatforms = relationship('DatasetsToPlatforms',
                                       backref='Datasets',
                                       post_update=True)
    DatasetsToOrganisms = relationship('DatasetsToOrganisms',
                                       backref='Datasets',
                                       post_update=True)
    DatasetsToDatatypes = relationship('DatasetsToDatatypes',
                                       backref='Datasets',
                                       post_update=True)
    DatasetsToDiseases = relationship('DatasetsToDiseases',
                                      backref='Datasets',
                                      post_update=True)

    def __repr__(self):
        return '<Datasets %r>' % (self.Accession)


class DatasetsToSamples(db.Model):
    __tablename__ = 'DatasetsToSamples'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    DatasetId = db.Column(INTEGER(unsigned=True),
                          db.ForeignKey(
                              'Datasets.id',
                              ondelete='CASCADE'))
    SampleId = db.Column(INTEGER(unsigned=True),
                         db.ForeignKey('Samples.id',
                                       ondelete='CASCADE'))
    Samples = relationship('Samples',
                           backref='DatasetsToSamples',
                           post_update=True)

    def __repr__(self):
        return '<DataSetsToSamples %r>' % (self.id)


class DatasetsToPlatforms(db.Model):
    __tablename__ = 'DatasetsToPlatforms'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    DatasetId = db.Column(INTEGER(unsigned=True),
                          db.ForeignKey(
                              'Datasets.id',
                              ondelete='CASCADE'))
    PlatformId = db.Column(INTEGER(unsigned=True),
                           db.ForeignKey('Platforms.id',
                                         ondelete='CASCADE'))
    Platforms = relationship('Platforms',
                             backref='DatasetsToPlatforms',
                             post_update=True)

    def __repr__(self):
        return '<DataSetsToPlatforms %r>' % (self.id)


class DatasetsToOrganisms(db.Model):
    __tablename__ = 'DatasetsToOrganisms'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    DatasetId = db.Column(INTEGER(unsigned=True),
                          db.ForeignKey(
                              'Datasets.id',
                              ondelete='CASCADE'))
    OrganismId = db.Column(INTEGER(unsigned=True),
                           db.ForeignKey('Organisms.id',
                                         ondelete='CASCADE'))
    Organisms = relationship('Organisms',
                             backref='DatasetsToOrganisms',
                             post_update=True)

    def __repr__(self):
        return '<DataSetsToOrganisms %r>' % (self.id)


class DatasetsToDatatypes(db.Model):
    __tablename__ = 'DatasetsToDatatypes'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    DatasetId = db.Column(INTEGER(unsigned=True),
                          db.ForeignKey(
                              'Datasets.id',
                              ondelete='CASCADE'))
    DatatypeId = db.Column(INTEGER(unsigned=True),
                           db.ForeignKey('Datatypes.id',
                                         ondelete='CASCADE'))
    Datatypes = relationship('Datatypes',
                             backref='DatasetsToDatatypes',
                             post_update=True)

    def __repr__(self):
        return '<DataSetsToDatatypes %r>' % (self.id)


class DatasetsToDiseases(db.Model):
    __tablename__ = 'DatasetsToDiseases'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    DatasetId = db.Column(INTEGER(unsigned=True),
                          db.ForeignKey(
                              'Datasets.id',
                              ondelete='CASCADE'))
    DiseaseId = db.Column(INTEGER(unsigned=True),
                          db.ForeignKey('Diseases.id',
                                        ondelete='CASCADE'))
    Diseases = relationship('Diseases',
                            backref='DatasetsToDiseases',
                            post_update=True)

    def __repr__(self):
        return '<DataSetsToDatatypes %r>' % (self.id)


class Samples(db.Model):
    __tablename__ = 'Samples'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    Accession = db.Column(VARCHAR(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Samples %r>' % (self.Accession)


class Platforms(db.Model):
    __tablename__ = 'Platforms'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    Accession = db.Column(VARCHAR(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Platforms %r>' % (self.Accession)


class Organisms(db.Model):
    __tablename__ = 'Organisms'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    Name = db.Column(VARCHAR(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Organisms %r>' % (self.Name)


class Datatypes(db.Model):
    __tablename__ = 'Datatypes'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    Name = db.Column(VARCHAR(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Datatypes %r>' % (self.Name)


class Diseases(db.Model):
    __tablename__ = 'Diseases'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    Name = db.Column(VARCHAR(100), unique=True, nullable=False)
    Description = db.Column(VARCHAR(255), unique=True)
    TrustedBool = db.Column(BOOLEAN, nullable=False)

    def __repr__(self):
        return '<Organisms %r>' % (self.Name)

# -------------- Extractions to GeneLists/DEMs to Genes -----------------------


class ExtractionsToGeneLists(db.Model):
    __tablename__ = 'ExtractionsToGeneLists'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    ExtractionId = db.Column(INTEGER(unsigned=True),
                             db.ForeignKey(
                                 'Extractions.id',
                                 ondelete='CASCADE'))
    GeneListId = db.Column(INTEGER(unsigned=True),
                           db.ForeignKey('GeneLists.id',
                                         ondelete='CASCADE'))
    GeneLists = relationship('GeneLists',
                             backref='ExtractionsToGeneLists',
                             post_update=True)

    def __repr__(self):
        return '<ExtractionsToGeneLists %r>' % (self.id)


class ExtractionsToDEMs(db.Model):
    __tablename__ = 'ExtractionsToDEMs'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    ExtractionId = db.Column(INTEGER(unsigned=True),
                             db.ForeignKey(
                                 'Extractions.id',
                                 ondelete='CASCADE'))
    DEMId = db.Column(INTEGER(unsigned=True),
                      db.ForeignKey('DEMs.id',
                                    ondelete='CASCADE'))
    DEMs = relationship('DEMs',
                        backref='ExtractionsToDEMs',
                        post_update=True)

    def __repr__(self):
        return '<ExtractionsToDEMs %r>' % (self.id)


class GeneLists(db.Model):
    __tablename__ = 'GeneLists'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    EnrichrLink = db.Column(db.Text)
    Cutoff = db.Column(db.Integer)
    GeneListsToDEMsId = db.Column(INTEGER(unsigned=True),
                                  db.ForeignKey('GeneListsToDEMs.id',
                                                ondelete='CASCADE'))
    GeneListsToDEMs = relationship('GeneListsToDEMs',
                                   backref='GeneLists',
                                   post_update=True)

    def __repr__(self):
        return '<GeneLists %r>' % (self.id)


class GeneListsToGenes(db.Model):
    __tablename__ = 'GeneListsToGenes'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    PValue = db.Column(FLOAT)
    UpBool = db.Column(BOOLEAN)
    GeneId = db.Column(INTEGER(unsigned=True),
                       db.ForeignKey('Genes.id',
                                     ondelete='CASCADE'))
    GeneListsGenes = relationship('Gene',
                             backref='GeneListsToGenes',
                             post_update=True)

    def __repr__(self):
        return '<GeneListsToGenes %r>' % (self.id)


class GeneListsToDEMs(db.Model):
    __tablename__ = 'GeneListsToDEMs'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    DEMId = db.Column(INTEGER(unsigned=True),
                      db.ForeignKey('DEMs.id',
                                    ondelete='CASCADE'))
    GeneListsDEMs = relationship('DEMs',
                             backref='GeneListsToDEMs',
                             post_update=True)

    def __repr__(self):
        return '<GeneListsToDEMs %r>' % (self.id)


class Gene(db.Model):
    __tablename__ = 'Genes'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    Symbol = db.Column(VARCHAR(20), unique=True, nullable=False)
    
    def __init__(self, Symbol):
    	self.Symbol = Symbol

    def __repr__(self):
        return '<Gene %r>' % (self.Symbol)


class DEMs(db.Model):
    __tablename__ = 'DEMs'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    Name = db.Column(VARCHAR(50), unique=True, nullable=False)

    def __repr__(self):
        return '<DEMs %r>' % (self.Name)

# ---------------------- Extractions to Cells ---------------------------------


class ExtractionsToCells(db.Model):
    __tablename__ = 'ExtractionsToCells'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    ExtractionId = db.Column(INTEGER(unsigned=True),
                             db.ForeignKey(
                                 'Extractions.id',
                                 ondelete='CASCADE'))
    CellId = db.Column(INTEGER(unsigned=True),
                       db.ForeignKey('Cells.id',
                                     ondelete='CASCADE'))
    Cells = relationship('Cells',
                         backref='ExtractionsToCells',
                         post_update=True)

    def __repr__(self):
        return '<ExtractionsToCells %r>' % (self.id)


class Cells(db.Model):
    __tablename__ = 'Cells'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    Name = db.Column(VARCHAR(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Cells %r>' % (self.Name)

# ------------------ Extractions to Perturbations -----------------------------


class ExtractionsToPerturbations(db.Model):
    __tablename__ = 'ExtractionsToPerturbations'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    ExtractionId = db.Column(INTEGER(unsigned=True),
                             db.ForeignKey(
                                 'Extractions.id',
                                 ondelete='CASCADE'))
    PerturbationId = db.Column(INTEGER(unsigned=True),
                               db.ForeignKey('Perturbations.id',
                                             ondelete='CASCADE'))
    Perturbations = relationship('Perturbations',
                                 backref='ExtractionsToPerturbations')

    def __repr__(self):
        return '<ExtractionsToPerturbations %r>' % (self.id)


class Perturbations(db.Model):
    __tablename__ = 'Perturbations'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    Name = db.Column(VARCHAR(255), unique=True, nullable=False)

    def __repr__(self):
        return '<Perturbations %r>' % (self.Name)
