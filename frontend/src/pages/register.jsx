import { useState } from "react"

function Register() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    phone_number: "",
  })

  const [errors, setErrors] = useState({})
  const [message, setMessage] = useState("")
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target

    setFormData({
      ...formData,
      [name]: value,
    })

    // Remove error for the field when user starts correcting it
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: "",
      })
    }

    setMessage("")
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    setErrors({})
    setMessage("")
    setLoading(true)

    try {
      const response = await fetch(
        "http://localhost:8001/api/v1/auth/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        const fieldErrors = {}

        // FastAPI / Pydantic validation errors
        if (Array.isArray(data.detail)) {
          data.detail.forEach((error) => {
            const field = error.loc[error.loc.length - 1]

            fieldErrors[field] = error.msg
          })
        }

        // Custom backend error
        else if (typeof data.detail === "string") {
          setMessage(data.detail)
        }

        // Other error format
        else if (data.message) {
          setMessage(data.message)
        }

        setErrors(fieldErrors)

        return
      }

      // Registration successful
      setMessage("Registration successful!")

      setFormData({
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        phone_number: "",
      })
    } catch (error) {
      setMessage(
        error.message || "Unable to connect to the server"
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg">

        {/* Heading */}
        <h1 className="text-3xl font-bold text-center">
          ShopSphere
        </h1>

        <p className="mt-2 text-center text-gray-500">
          Create your account
        </p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-5">

          {/* Email */}
          <div>
            <label className="mb-2 block text-sm font-medium">
              Email
            </label>

            <input
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="you@example.com"
              required
              className={`w-full rounded-lg border px-4 py-3 outline-none ${
                errors.email
                  ? "border-red-500"
                  : "focus:border-blue-500"
              }`}
            />

            {errors.email && (
              <p className="mt-1 text-sm text-red-600">
                {errors.email}
              </p>
            )}
          </div>

          {/* Password */}
          <div>
            <label className="mb-2 block text-sm font-medium">
              Password
            </label>

            <input
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              required
              className={`w-full rounded-lg border px-4 py-3 outline-none ${
                errors.password
                  ? "border-red-500"
                  : "focus:border-blue-500"
              }`}
            />

            {errors.password && (
              <p className="mt-1 text-sm text-red-600">
                {errors.password}
              </p>
            )}
          </div>

          {/* First Name */}
          <div>
            <label className="mb-2 block text-sm font-medium">
              First Name
            </label>

            <input
              name="first_name"
              type="text"
              value={formData.first_name}
              onChange={handleChange}
              placeholder="Abhay"
              required
              className={`w-full rounded-lg border px-4 py-3 outline-none ${
                errors.first_name
                  ? "border-red-500"
                  : "focus:border-blue-500"
              }`}
            />

            {errors.first_name && (
              <p className="mt-1 text-sm text-red-600">
                {errors.first_name}
              </p>
            )}
          </div>

          {/* Last Name */}
          <div>
            <label className="mb-2 block text-sm font-medium">
              Last Name
            </label>

            <input
              name="last_name"
              type="text"
              value={formData.last_name}
              onChange={handleChange}
              placeholder="Kushwaha"
              required
              className={`w-full rounded-lg border px-4 py-3 outline-none ${
                errors.last_name
                  ? "border-red-500"
                  : "focus:border-blue-500"
              }`}
            />

            {errors.last_name && (
              <p className="mt-1 text-sm text-red-600">
                {errors.last_name}
              </p>
            )}
          </div>

          {/* Phone Number */}
          <div>
            <label className="mb-2 block text-sm font-medium">
              Phone Number
            </label>

            <input
              name="phone_number"
              type="tel"
              value={formData.phone_number}
              onChange={handleChange}
              placeholder="9876543210"
              required
              className={`w-full rounded-lg border px-4 py-3 outline-none ${
                errors.phone_number
                  ? "border-red-500"
                  : "focus:border-blue-500"
              }`}
            />

            {errors.phone_number && (
              <p className="mt-1 text-sm text-red-600">
                {errors.phone_number}
              </p>
            )}
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading
              ? "Creating Account..."
              : "Create Account"}
          </button>

        </form>

        {/* General Message */}
        {message && (
          <p
            className={`mt-5 text-center text-sm font-medium ${
              message === "Registration successful!"
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            {message}
          </p>
        )}

      </div>
    </div>
  )
}

export default Register