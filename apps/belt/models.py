from django.db import models
import re 
import bcrypt 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, data):
        errors = {}
        #name check
        if len(data['name']) < 1:
            errors["Name"] = "invalid name"
        # #last name check   
        if not data['alias'].isalpha():
            errors["alias"] = "invalid alias"
        # #email check
        if len(data['email']) < 1 or not EMAIL_REGEX.match(data['email']):
            errors["email"] = "invalid email"
        #duplicate email check
        else:
            duplicate = User.objects.filter(email=data['email'])
            if duplicate:
                errors["email"] = "email already registered"
        #password check
        if len(data['password']) < 8:
            errors["confirmPassword"] = "invalid password"
        elif data['password'] != data['confirmPassword']:   
            errors["confirmPassword"] = "passwords must match"
        return errors

    def register(self, data):
        pw = data['password'] 
        hashedpw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        hashedpw = (str(hashedpw)).split("'")[1]
        User.objects.create(name=data['name'], alias=data['alias'], email=data['email'], password=hashedpw, dateOfBirth=data['dateOfBirth'])
    
    def validate_login(self, data):
        user = User.objects.filter(email=data['loginEmail'])
        if user:
            checkAgainst = User.objects.get(email=data['loginEmail']).password
            if bcrypt.checkpw(data['loginPassword'].encode(), checkAgainst.encode()):
                return User.objects.get(email=data['loginEmail']).id
        print("password failed") 
        return False

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dateOfBirth = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
        #Many to Many
    relationships = models.ManyToManyField("self", through="Relationship", symmetrical=False, related_name="related_to")
    objects = UserManager()

class Relationship(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_people')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_people")


















