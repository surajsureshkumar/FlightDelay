db.delays.aggregate([
    {
        $match:
            {
                $and: [
                    { departure_delay: { $gt: 30 } },
                    { arrival_delay: { $gt: 30 } },
                    { OP_CARRIER: { $in: ['AA', 'DL', 'UA'] } }
                ]
            }
    },
    {
        $project: {
            OP_CARRIER: 1,
            flight_date: 1,
            origin: 1,
            destination: 1,
            OP_CARRIER_FL_NUM: { $substr: ["$OP_CARRIER_FL_NUM", 0, -1] }
        }
    },
    {
        $project: {
            flight_number: {
                $concat: ["$OP_CARRIER", "$OP_CARRIER_FL_NUM"]
            },
            flight_date: 1,
            origin: 1,
            destination: 1
        }
    },
    { $out: "major_airlines" }
])



db.major_airlines.aggregate([
    {
        $group: {
            _id: { destination: "$destination", flight_date: "$flight_date", origin: "$origin", flight_number: "$flight_number" },
            uniqueIds: { $addToSet: "$_id" },
            doc: { $first: "$$ROOT" }
        }
    },
    {
        $replaceRoot: {
            newRoot: "$doc"
        }
    }
], { allowDiskUse: true }).forEach(function (doc) {
    db.temp.insertOne(doc);
});
