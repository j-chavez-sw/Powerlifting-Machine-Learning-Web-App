from Capstone.ML.predict_squat import predict_squat
from Capstone.ML.predict_deadlift import predict_deadlift
from Capstone.ML.predict_bench import predict_bench

pb = predict_bench()
pd = predict_deadlift()
ps = predict_squat()

pb.train_create_model()
pd.train_create_model()
ps.train_create_model()