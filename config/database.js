const mongoose = require('mongoose').default;

const connectDB = async () => {
    try {
        const connection = await mongoose.connect(
            'mongodb+srv://wkmswanthra:wkmswanthra@test-bed.dtgmi5a.mongodb.net/test'
        )

        console.log(`MongoDB connection: ${connection.connection.host}`)
    } catch (e) {
        console.log(e)
        process.exit(1)
    }
}

module.exports = connectDB