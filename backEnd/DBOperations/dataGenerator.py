import random
import mysql.connector
from faker import Faker
from decouple import config

db = mysql.connector.connect(
    host="localhost",
    user=config("DB_USER"),
    password=config("DB_PASSWORD"),
    port=3306,
    database="health_fitness"
)

cursor = db.cursor()
fake = Faker()

class CreateSyntheticData:
    
    def __init__(self):
        return

    def createDataBase(self):
        cursor.execute("""CREATE DATABASE IF NOT EXISTS health_fitness""")

    def create_tables(self):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                email VARCHAR(255),
                age INT,
                gender ENUM('Male', 'Female', 'Other')
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Workouts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                workout_date DATE,
                duration_minutes INT,
                workout_type VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES Users(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Exercises (
                id INT AUTO_INCREMENT PRIMARY KEY,
                workout_id INT,
                exercise_name VARCHAR(255),
                sets INT,
                reps_per_set INT,
                FOREIGN KEY (workout_id) REFERENCES Workouts(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Nutrition (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                meal_date DATE,
                calories INT,
                protein_grams INT,
                fat_grams INT,
                carbs_grams INT,
                FOREIGN KEY (user_id) REFERENCES Users(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS HealthMetrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                metric_date DATE,
                weight_kg DECIMAL(5, 2),
                body_fat_percentage DECIMAL(4, 2),
                resting_heart_rate INT,
                FOREIGN KEY (user_id) REFERENCES Users(id)
            )
        """)

    def populate_users(self, num_users=10):
        for _ in range(num_users):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            age = random.randint(18, 60)
            gender = random.choice(['Male', 'Female', 'Other'])

            cursor.execute("""
                INSERT INTO Users (first_name, last_name, email, age, gender) 
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, email, age, gender))
        db.commit()

    def populate_workouts(self, num_workouts=30):
        cursor.execute("SELECT id FROM Users")
        user_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(num_workouts):
            user_id = random.choice(user_ids)
            workout_date = fake.date_this_year()
            duration_minutes = random.randint(20, 120)
            workout_type = random.choice(['Cardio', 'Strength', 'Yoga', 'CrossFit'])

            cursor.execute("""
                INSERT INTO Workouts (user_id, workout_date, duration_minutes, workout_type)
                VALUES (%s, %s, %s, %s)
            """, (user_id, workout_date, duration_minutes, workout_type))
        db.commit()

    def populate_exercises(self, num_exercises=50):
        cursor.execute("SELECT id FROM Workouts")
        workout_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(num_exercises):
            workout_id = random.choice(workout_ids)
            exercise_name = random.choice(['Push Ups', 'Squats', 'Pull Ups', 'Deadlifts', 'Lunges'])
            sets = random.randint(2, 5)
            reps_per_set = random.randint(8, 15)

            cursor.execute("""
                INSERT INTO Exercises (workout_id, exercise_name, sets, reps_per_set)
                VALUES (%s, %s, %s, %s)
            """, (workout_id, exercise_name, sets, reps_per_set))
        db.commit()

    def populate_nutrition(self, num_entries=30):
        cursor.execute("SELECT id FROM Users")
        user_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(num_entries):
            user_id = random.choice(user_ids)
            meal_date = fake.date_this_year()
            calories = random.randint(400, 1500)
            protein_grams = random.randint(20, 100)
            fat_grams = random.randint(10, 60)
            carbs_grams = random.randint(50, 200)

            cursor.execute("""
                INSERT INTO Nutrition (user_id, meal_date, calories, protein_grams, fat_grams, carbs_grams)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, meal_date, calories, protein_grams, fat_grams, carbs_grams))
        db.commit()

    def populate_health_metrics(self, num_entries=20):
        cursor.execute("SELECT id FROM Users")
        user_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(num_entries):
            user_id = random.choice(user_ids)
            metric_date = fake.date_this_year()
            weight_kg = round(random.uniform(50, 120), 2)
            body_fat_percentage = round(random.uniform(10, 30), 2)
            resting_heart_rate = random.randint(50, 90)

            cursor.execute("""
                INSERT INTO HealthMetrics (user_id, metric_date, weight_kg, body_fat_percentage, resting_heart_rate)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, metric_date, weight_kg, body_fat_percentage, resting_heart_rate))
        db.commit()

    def executor(self):
        self.createDataBase()
        self.create_tables()
        self.populate_users()
        self.populate_workouts()
        self.populate_exercises()
        self.populate_nutrition()
        self.populate_health_metrics()

    print("Database populated with fake data.")
