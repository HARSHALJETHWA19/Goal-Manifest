import React, { useState } from "react";

const EmailForm = () => {
  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = {
      recipient_email: email,
    };

    try {
      const response = await fetch(
        "<API-Gateway URL>",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      );

      const data = await response.json();
      if (response.ok) {
        alert(data.message); // Success message
      } else {
        alert("There was an error sending the email.");
      }
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-400 via-blue-500 to-purple-600 flex items-center justify-center p-4">
      <div className="bg-white shadow-2xl rounded-lg p-8 md:p-12 max-w-lg w-full">
        <h1 className="text-3xl md:text-4xl font-bold text-center text-gray-800 mb-8">
          📧 Send Goal & Motivation
        </h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="email"
              className="block text-lg font-medium text-gray-700 mb-2"
            >
              Recipient Email:
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full p-3 border border-gray-300 rounded-lg shadow-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter recipient's email"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white py-3 px-6 rounded-lg font-bold text-lg shadow-lg hover:shadow-xl hover:scale-105 transform transition-all duration-300 focus:ring-4 focus:ring-purple-300"
          >
            Send Email 🚀
          </button>
        </form>
        <p className="text-center text-gray-500 mt-8 text-sm">
          Make someone's day with a goal and some motivation! 💪
        </p>
      </div>
    </div>
  );
};

export default EmailForm;
