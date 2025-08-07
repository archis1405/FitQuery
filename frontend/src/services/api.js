import axios from "axios";

export const fetchData = async (question) => {
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/fetch-data",
      { query: question },
      {
        headers: {
          "Content-Type": "application/json",
        },
        // params can be used to send query string params
        //   params: { question }
      }
    );
    console.log("Response in api:::", response.data.SQLQuery);
    return response.data;
  } catch (error) {
    console.error("Error fetching generated query:", error);
    throw error;
  }
};
