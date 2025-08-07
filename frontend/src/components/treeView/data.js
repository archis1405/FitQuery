export const files = {
  name: "heath_fitness",
  isFolder: true,
  isDB: true,
  children: [
    {
      name: "users",
      isFolder: true,
      children: [
        {
          name: "id - integer",
          isFolder: false,
        },
        {
          name: "firstname - varchar",
          isFolder: false,
        },
        {
          name: "lastname - varchar",
          isFolder: false,
        },
        {
          name: "email - varchar",
          isFolder: false,
        },
        {
          name: "age - integer",
          isFolder: false,
        },
        {
          name: "gender - enum",
          isFolder: false,
        },
      ],
    },
    {
      name: "workouts",
      isFolder: true,
      children: [
        {
          name: "id - integer",
          isFolder: false,
        },
        {
          name: "user_id - integer",
          isFolder: false,
        },
        {
          name: "workout_type - varchar",
          isFolder: false,
        },
        {
          name: "duration - integer",
          isFolder: false,
        },
        {
          name: "calories_burned - float",
          isFolder: false,
        },
        {
          name: "date - datetime",
          isFolder: false,
        },
      ],
    },
    {
      name: "embeddings",
      isFolder: true,
      children: [
        {
          name: "id - integer",
          isFolder: false,
        },
        {
          name: "entity_type - enum",
          isFolder: false,
        },
        {
          name: "column_name - varchar",
          isFolder: false,
        },
        {
          name: "embedding - blob",
          isFolder: false,
        },
      ],
    },
    {
      name: "exercises",
      isFolder: true,
      children: [
        {
          name: "id - integer",
          isFolder: false,
        },
        {
          name: "workout_id - integer",
          isFolder: false,
        },
        {
          name: "excercise_name - varchar",
          isFolder: false,
        },
        {
          name: "sets - integer",
          isFolder: false,
        },
        {
          name: "reps_per_set - integer",
          isFolder: false,
        },
      ],
    },
    {
      name: "healthmetrics",
      isFolder: true,
      children: [
        {
          name: "id - integer",
          isFolder: false,
        },
        {
          name: "user_id - integer",
          isFolder: false,
        },
        {
          name: "metric_date - date",
          isFolder: false,
        },
        {
          name: "weight_kg - decimal",
          isFolder: false,
        },
        {
          name: "body_fat_percentage - decimal",
          isFolder: false,
        },
        {
          name: "resting_heart_rate - integer",
          isFolder: false,
        },
      ],
    },
    {
      name: "nutrition",
      isFolder: true,
      children: [
        {
          name: "id - integer",
          isFolder: false,
        },
        {
          name: "user_id - integer",
          isFolder: false,
        },
        {
          name: "meal_date - date",
          isFolder: false,
        },
        {
          name: "calories - integers",
          isFolder: false,
        },
        {
          name: "protein_grams - integer",
          isFolder: false,
        },
        {
          name: "fat_grams - integer",
          isFolder: false,
        },
        {
          name: "carbs_gram - integer",
          isFolder: false,
        },
      ],
    },
  ],
};
