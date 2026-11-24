from db import engine, Base
import models  # must be imported so Base knows about every table

Base.metadata.create_all(engine)
print("Tables created.")