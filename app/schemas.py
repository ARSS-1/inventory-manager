from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    ConfigDict,
    AfterValidator,
    BeforeValidator,
    NonNegativeInt,
    NonNegativeFloat,
)
from typing import Annotated, List, Optional


def set_lowcase(name: str) -> str:
    return name.lower().strip()


def set_capitalize(name: str) -> str:
    return name.title()


def extrac_names(products):
    return [product.name for product in products] if products else []


class ProductBase(BaseModel):

    name: Annotated[
        str, Field(description="Product", max_length=100), AfterValidator(set_lowcase)
    ]
    quantity: Annotated[NonNegativeInt, Field(description="Quantity", default=0)]
    price: Annotated[NonNegativeFloat, Field(description="Price", default=1.0)]
    description: Annotated[
        Optional[str], Field(description="Description", default=None)
    ]


class ProductIn(ProductBase):
    pass


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: Annotated[PositiveInt, Field(description="ID")]

    name: Annotated[
        str,
        Field(description="Product"),
        AfterValidator(set_capitalize),
    ]


class ProductUpdate(BaseModel):
    name: Annotated[
        Optional[str],
        Field(description="Product", max_length=100, default=None),
        AfterValidator(set_lowcase),
    ]
    quantity: Annotated[
        Optional[NonNegativeInt], Field(description="Quantity", default=None)
    ]
    price: Annotated[
        Optional[NonNegativeFloat], Field(description="Price", default=None)
    ]
    description: Annotated[
        Optional[str], Field(description="Description", default=None)
    ]


class UserIn(BaseModel):
    username: Annotated[str, Field(description="Username", max_length=20)]
    password: Annotated[str, Field(description="Password", min_length=8, max_length=16)]


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Annotated[PositiveInt, Field(description="ID")]
    username: str
    products: Annotated[List[str], BeforeValidator(extrac_names)]
