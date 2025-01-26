db.major_airlines.aggregate([
    { "$group": { _id: "$flight_number", count: { $sum: 1 } } },
    { $match: { count: { $gt: 9 } } },
    {
        $project: {
            flight_number_1: "$_id",
            count: 1,
            _id: 0
        }
    },
    { $out: "l1" }
])
