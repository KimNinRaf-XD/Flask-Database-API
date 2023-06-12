from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__, template_folder="templates")

app.config["SECRET_KEY"] = "secret"
app.config["DEBUG"] = True
app.config["TESTING"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipehub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
api = Api(app)


# -------------------- Database Tables
class Accounts(db.Model):  # type: ignore
    __tablename__ = "Accounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class Recipes(db.Model):  # type: ignore
    __tablename__ = "Recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)


class UserRecipe(db.Model):  # type: ignore
    __tablename__ = "UserRecipe"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("Recipes.id"))
    account_id = db.Column(db.Integer, db.ForeignKey("Accounts.id"))


# -------------------- API Requests
# ---------- Accounts
class viewAccounts(Resource):
    def get(self):
        acc = Accounts.query.all()
        acc_ = []
        for a in acc:
            account = {}
            account["name"] = a.name
            account["username"] = a.username
            account["password"] = a.password
            acc_.append(account)
        return {"Accounts": acc_}


api.add_resource(viewAccounts, "/api/accounts")


class registerAccounts(Resource):
    def post(self):
        result = request.get_json()
        acc = Accounts(
            name=result["name"],
            username=result["username"],
            password=result["password"],
        )
        db.session.add(acc)
        db.session.commit()
        return {"message": "Account registered"}


api.add_resource(registerAccounts, "/api/register")


class deleteAccounts(Resource):
    def delete(self, id):
        acc = Accounts.query.filter_by(id=id).first()
        db.session.delete(acc)
        db.session.commit()
        return {"message": "Account removed"}


api.add_resource(deleteAccounts, "/api/delete-account/<id>")


class updateAccounts(Resource):
    def put(self, id):
        acc = Accounts.query.filter_by(id=id).first()
        result = request.get_json()
        acc.name = result.get("name", acc.name)
        acc.username = result.get("username", acc.username)
        acc.password = result.get("password", acc.password)
        db.session.add(acc)
        db.session.commit()
        return {"message": "Account info updated"}


api.add_resource(updateAccounts, "/api/update-account/<id>")


# ---------- Recipes
class viewRecipes(Resource):
    def get(self):
        rec = Recipes.query.all()
        rec_ = []
        for r in rec:
            recipe = {}
            recipe["name"] = r.name
            recipe["ingredients"] = r.ingredients
            recipe["instructions"] = r.instructions
            rec_.append(recipe)
        return {"Recipes": rec_}


api.add_resource(viewRecipes, "/api/recipes")


class addRecipes(Resource):
    def post(self):
        result = request.get_json()
        rec = Recipes(
            name=result["name"],
            ingredients=result["ingredients"],
            instructions=result["instructions"],
        )
        db.session.add(rec)
        db.session.commit()
        return {"message": "Recipe added"}


api.add_resource(addRecipes, "/api/add-recipe")


class deleteRecipes(Resource):
    def delete(self, id):
        rec = Recipes.query.filter_by(id=id).first()
        db.session.delete(rec)
        db.session.commit()
        return {"message": "Recipe removed"}


api.add_resource(deleteRecipes, "/api/delete-recipe/<id>")


class updateRecipes(Resource):
    def put(self, id):
        rec = Recipes.query.filter_by(id=id).first()
        result = request.get_json()
        rec.name = result.get("name", rec.name)
        rec.ingredients = result.get("ingredients", rec.ingredients)
        rec.instructions = result.get("instructions", rec.instructions)
        db.session.add(rec)
        db.session.commit()
        return {"message": "Recipe updated"}


api.add_resource(updateRecipes, "/api/update-recipe/<id>")


# -------------------- Routes
@app.route("/")
def index():
    account = Accounts.query.all()
    recipe = Recipes.query.all()
    return render_template("index.html", account=account, recipe=recipe)


if __name__ == "__main__":
    app.run()
