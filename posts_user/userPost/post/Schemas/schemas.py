from pydantic import BaseModel, Field, constr, validator, EmailStr
from enum import Enum
from typing import Optional, List
import string

class postEnum(str, Enum):
    published = "published"
    draft = "draft"

class Post(BaseModel):
    tittle: str
    @validator("tittle")
    def validate_tittle(cls, tittle):
        if tittle is None:
            raise ValueError("tittle cannot be empty")
        return tittle
    body: str
    @validator("body")
    def validate_body(cls, body):
        if body is None:
            raise ValueError("body cannot be empty")
        return body
    User_id: int
    @validator("User_id")
    def validate_user_id(cls, user_id):
        if user_id is None:
            raise ValueError("User_id cannot be empty")
        return user_id
    status: postEnum = Field(default="draft")

class Postdesc(BaseModel):
    tittle: str
    body: str
    class Config():
        orm_mode = True


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"

class User(BaseModel):
    firstname: constr(min_length=2, max_length=50)
    lastname: constr(min_length=2, max_length=50)
    email: EmailStr
    mobile: str
    
    @validator("mobile")
    def validate_mobile(cls, mobile):
        if not mobile.isdigit() or len(mobile) != 10:
            raise ValueError("Mobile number must be exactly 10 digits and contain no non-digit characters.")
        return mobile
    
    gender: GenderEnum = Field(default="male")
    password: constr(min_length=6, max_length=20)
    
    @validator("password")
    def validate_password(cls, password):
        # Check minimum length
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        # Check maximum length
        if len(password) > 20:
            raise ValueError("Password cannot exceed 20 characters")

        # Check for apostrophe
        if "'" in password:
            raise ValueError("Apostrophes are not allowed in the password")

        return password
    
    confirmpassword: constr(min_length=6, max_length=20)
    status: StatusEnum = Field(default="active")
    
    @validator("confirmpassword")
    def passwords_match(cls, confirmpassword, values):
        if "password" in values and confirmpassword != values["password"]:
            raise ValueError("Passwords do not match")
        return confirmpassword

class showUser(BaseModel):
    firstname: str
    lastname: str
    email: str
    mobile: int
    gender: GenderEnum
    posts: List[Postdesc] = []
    class Config():
        orm_mode = True

class showPost(BaseModel):
    tittle: str
    body: str
    creator: showUser
    class Config():
        orm_mode = True
    
    