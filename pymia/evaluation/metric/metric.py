"""The metric module provides a set of metrics."""
from .reconstruction import (PeakSignalToNoiseRatio, StructuralSimilarityIndexMeasure)
from .regression import (CoefficientOfDetermination, MeanAbsoluteError, MeanSquaredError, RootMeanSquaredError,
                         NormalizedRootMeanSquaredError)
from .segmentation import (Accuracy, AdjustedRandIndex, AreaUnderCurve, AverageDistance, CohenKappaCoefficient,
                           DiceCoefficient, FalseNegative, FalsePositive, Fallout, FalseNegativeRate, FMeasure,
                           GlobalConsistencyError, GroundTruthVolume, HausdorffDistance,
                           InterclassCorrelation, JaccardCoefficient, MahalanobisDistance, MutualInformation, Precision,
                           ProbabilisticDistance, RandIndex, SegmentationVolume,
                           Sensitivity, Specificity, SurfaceDiceOverlap, SurfaceOverlap, TrueNegative, TruePositive,
                           VariationOfInformation, VolumeSimilarity)


def get_reconstruction_metrics():
    """Gets a list with reconstruction metrics.

    Returns:
        list[Metric]: A list of metrics.
    """
    return [PeakSignalToNoiseRatio(), StructuralSimilarityIndexMeasure()]


def get_segmentation_metrics():
    """Gets a list with segmentation metrics.

    Returns:
        list[Metric]: A list of metrics.
    """
    return get_overlap_metrics() + get_distance_metrics() + get_classical_metrics()


def get_regression_metrics():
    """Gets a list with all regression metrics.

    Returns:
        list[Metric]: A list of metrics.
    """
    return [CoefficientOfDetermination(), MeanAbsoluteError(), MeanSquaredError(), RootMeanSquaredError(),
            NormalizedRootMeanSquaredError()]


def get_overlap_metrics():
    """Gets a list of overlap-based metrics.

    Returns:
        list[Metric]: A list of metrics.
    """
    return [AdjustedRandIndex(),
            AreaUnderCurve(),
            CohenKappaCoefficient(),
            DiceCoefficient(),
            InterclassCorrelation(),
            JaccardCoefficient(),
            MutualInformation(),
            RandIndex(),
            SurfaceOverlap(),
            SurfaceDiceOverlap(),
            VolumeSimilarity()]


def get_distance_metrics():
    """Gets a list of distance-based metrics.

    Returns:
        list[Metric]: A list of metrics.
    """

    return [HausdorffDistance(),
            AverageDistance(),
            MahalanobisDistance(),
            VariationOfInformation(),
            GlobalConsistencyError(),
            ProbabilisticDistance()]


def get_classical_metrics():
    """Gets a list of classical metrics.

    Returns:
        list[Metric]: A list of metrics.
    """

    return[Sensitivity(),
           Specificity(),
           Precision(),
           FMeasure(),
           Accuracy(),
           Fallout(),
           FalseNegativeRate(),
           TruePositive(),
           FalsePositive(),
           TrueNegative(),
           FalseNegative(),
           GroundTruthVolume(),
           SegmentationVolume()]
