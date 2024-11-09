# Import core types
from __future__ import annotations

from enum import Enum
from typing import Annotated, List, Literal, Optional, Self, Union

# Import aind-datas-schema types
from pydantic import BaseModel, Field, NonNegativeFloat, field_validator, model_validator
from typing_extensions import TypeAliasType


class TruncationParameters(BaseModel):
    is_truncated: bool = Field(default=False, description="Whether the distribution is truncated")
    min: float = Field(default=0, description="Minimum value of the sampled distribution")
    max: float = Field(default=0, description="Maximum value of the sampled distribution")


class ScalingParameters(BaseModel):
    scale: float = Field(default=1, description="Scaling factor to apply on the sampled distribution")
    offset: float = Field(default=0, description="Offset factor to apply on the sampled distribution")


class DistributionFamily(str, Enum):
    SCALAR = "Scalar"
    NORMAL = "Normal"
    LOGNORMAL = "LogNormal"
    UNIFORM = "Uniform"
    EXPONENTIAL = "Exponential"
    GAMMA = "Gamma"
    BINOMIAL = "Binomial"
    BETA = "Beta"
    POISSON = "Poisson"
    PDF = "Pdf"


class DistributionParametersBase(BaseModel):
    family: DistributionFamily = Field(..., description="Family of the distribution")


class DistributionBase(BaseModel):
    family: DistributionFamily = Field(..., description="Family of the distribution")
    distribution_parameters: DistributionParameters = Field(..., description="Parameters of the distribution")
    truncation_parameters: Optional[TruncationParameters] = Field(
        default=None, description="Truncation parameters of the distribution"
    )
    scaling_parameters: Optional[ScalingParameters] = Field(
        default=None, description="Scaling parameters of the distribution"
    )


class ScalarDistributionParameter(DistributionParametersBase):
    family: Literal[DistributionFamily.SCALAR] = DistributionFamily.SCALAR
    value: float = Field(default=0, description="The static value of the distribution")


class Scalar(DistributionBase):
    family: Literal[DistributionFamily.SCALAR] = DistributionFamily.SCALAR
    distribution_parameters: ScalarDistributionParameter = Field(
        default=ScalarDistributionParameter(), description="Parameters of the distribution"
    )
    truncation_parameters: Literal[None] = None
    scaling_parameters: Literal[None] = None


class NormalDistributionParameters(DistributionParametersBase):
    family: Literal[DistributionFamily.NORMAL] = DistributionFamily.NORMAL
    mean: float = Field(default=0, description="Mean of the distribution")
    std: float = Field(default=0, description="Standard deviation of the distribution")


class NormalDistribution(DistributionBase):
    family: Literal[DistributionFamily.NORMAL] = DistributionFamily.NORMAL
    distribution_parameters: NormalDistributionParameters = Field(
        default=NormalDistributionParameters(), description="Parameters of the distribution"
    )


class LogNormalDistributionParameters(DistributionParametersBase):
    family: Literal[DistributionFamily.LOGNORMAL] = DistributionFamily.LOGNORMAL
    mean: float = Field(default=0, description="Mean of the distribution")
    std: float = Field(default=0, description="Standard deviation of the distribution")


class LogNormalDistribution(DistributionBase):
    family: Literal[DistributionFamily.LOGNORMAL] = DistributionFamily.LOGNORMAL
    distribution_parameters: LogNormalDistributionParameters = Field(
        default=LogNormalDistributionParameters(), description="Parameters of the distribution"
    )


class UniformDistributionParameters(DistributionParametersBase):
    family: Literal[DistributionFamily.UNIFORM] = DistributionFamily.UNIFORM
    min: float = Field(default=0, description="Minimum value of the distribution")
    max: float = Field(default=0, description="Maximum value of the distribution")


class UniformDistribution(DistributionBase):
    family: Literal[DistributionFamily.UNIFORM] = DistributionFamily.UNIFORM
    distribution_parameters: UniformDistributionParameters = Field(
        default=UniformDistributionParameters(), description="Parameters of the distribution"
    )


class ExponentialDistributionParameters(DistributionParametersBase):
    family: Literal[DistributionFamily.EXPONENTIAL] = DistributionFamily.EXPONENTIAL
    rate: float = Field(default=0, ge=0, description="Rate parameter of the distribution")


class ExponentialDistribution(DistributionBase):
    family: Literal[DistributionFamily.EXPONENTIAL] = DistributionFamily.EXPONENTIAL
    distribution_parameters: ExponentialDistributionParameters = Field(
        default=ExponentialDistributionParameters(), description="Parameters of the distribution"
    )


class GammaDistributionParameters(DistributionParametersBase):
    family: Literal[DistributionFamily.GAMMA] = DistributionFamily.GAMMA
    shape: float = Field(default=1, ge=0, description="Shape parameter of the distribution")
    rate: float = Field(default=1, ge=0, description="Rate parameter of the distribution")


class GammaDistribution(DistributionBase):
    family: Literal[DistributionFamily.GAMMA] = DistributionFamily.GAMMA
    distribution_parameters: GammaDistributionParameters = Field(
        default=GammaDistributionParameters(), description="Parameters of the distribution"
    )


class BinomialDistributionParameters(DistributionParametersBase):
    family: Literal[DistributionFamily.BINOMIAL] = DistributionFamily.BINOMIAL
    n: int = Field(default=1, ge=0, description="Number of trials")
    p: float = Field(default=0.5, ge=0, le=1, description="Probability of success")


class BinomialDistribution(DistributionBase):
    family: Literal[DistributionFamily.BINOMIAL] = DistributionFamily.BINOMIAL
    distribution_parameters: BinomialDistributionParameters = Field(
        default=BinomialDistributionParameters(), description="Parameters of the distribution"
    )


class BetaDistributionParameters(DistributionParametersBase):
    family: Literal[DistributionFamily.BETA] = DistributionFamily.BETA
    alpha: float = Field(default=5, ge=0, description="Alpha parameter of the distribution")
    beta: float = Field(default=5, ge=0, description="Beta parameter of the distribution")


class BetaDistribution(DistributionBase):
    family: Literal[DistributionFamily.BETA] = DistributionFamily.BETA
    distribution_parameters: BetaDistributionParameters = Field(
        default=BetaDistributionParameters(), description="Parameters of the distribution"
    )


class PoissonDistributionParameters(DistributionParametersBase):
    family: Literal[DistributionFamily.POISSON] = DistributionFamily.POISSON
    rate: float = Field(
        default=1, ge=0, description="Rate parameter of the Poisson process that generates the distribution"
    )


class PoissonDistribution(DistributionBase):
    family: Literal[DistributionFamily.POISSON] = DistributionFamily.POISSON
    distribution_parameters: PoissonDistributionParameters = Field(
        default=PoissonDistributionParameters(), description="Parameters of the distribution"
    )


class PdfDistributionParameters(DistributionParametersBase):
    family: Literal[DistributionFamily.PDF] = DistributionFamily.PDF
    pdf: List[NonNegativeFloat] = Field(default=[1], description="The probability density function")
    index: List[float] = Field(default=[0], description="The index of the probability density function")

    @field_validator("pdf")
    @classmethod
    def normalize_pdf(cls, v: List[NonNegativeFloat]) -> List[NonNegativeFloat]:
        return [x / sum(v) for x in v]

    @model_validator(mode="after")
    def validate_matching_length(self) -> Self:
        if len(self.pdf) != len(self.index):
            raise ValueError("pdf and index must have the same length")
        return self


class PdfDistribution(DistributionBase):
    family: Literal[DistributionFamily.PDF] = DistributionFamily.PDF
    distribution_parameters: PdfDistributionParameters = Field(
        default=PdfDistributionParameters(),
        description="Parameters of the distribution",
        validate_default=True,
    )


Distribution = TypeAliasType(
    "Distribution",
    Annotated[
        Union[
            Scalar,
            NormalDistribution,
            LogNormalDistribution,
            ExponentialDistribution,
            UniformDistribution,
            PoissonDistribution,
            BinomialDistribution,
            BetaDistribution,
            GammaDistribution,
            PdfDistribution,
        ],
        Field(discriminator="family", title="Distribution", description="Available distributions"),
    ],
)

DistributionParameters = TypeAliasType(
    "DistributionParameters",
    Annotated[
        Union[
            ScalarDistributionParameter,
            NormalDistributionParameters,
            LogNormalDistributionParameters,
            ExponentialDistributionParameters,
            UniformDistributionParameters,
            PoissonDistributionParameters,
            BinomialDistributionParameters,
            BetaDistributionParameters,
            GammaDistributionParameters,
            PdfDistributionParameters,
        ],
        Field(discriminator="family", title="DistributionParameters", description="Parameters of the distribution"),
    ],
)
