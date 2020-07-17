{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "import numpy as np\n",
    "from datetime import datetime\n",
    "\n",
    "from flask import Flask, jsonify"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "Base = automap_base()\n",
    "Base.prepare(engine, reflect=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "measurement = Base.classes.measurement\n",
    "station = Base.classes.station"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/\")\n",
    "def surfs_up():\n",
    "    return (\n",
    "        f\"Welcome to the climate app<br/>\"\n",
    "        f\"Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/<start><br/>\"\n",
    "        f\"/api/v1.0/<start>/<end>`\"\n",
    "    )\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precipitation():\n",
    "    session = Session(engine)\n",
    "    start_date = dt.date(2016,8,23)\n",
    "    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > start_date).order_by(measurement.date).all()\n",
    "    session.close()\n",
    "    date_tobs = []                                                                   \n",
    "    for row in results:\n",
    "        dict = {}\n",
    "        dict['date'] = row.date\n",
    "        dict['tobs'] = row.tobs\n",
    "        date_tobs.append(dict)\n",
    "                                                                       \n",
    "    return jsonify(date_tobs)                                                                \n",
    "                                                                       \n",
    "                                                                       \n",
    "                                                         "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    session = Session(engine)\n",
    "    results = session.query(measurement.station, station.name).group_by(measurement.station).all()\n",
    "    session.close()\n",
    "    \n",
    "    station_list = []\n",
    "    for row in results:\n",
    "        dict={}\n",
    "        dict['name'] = row.name\n",
    "        dict['station'] = row.station\n",
    "        station_list.append(dict)\n",
    "\n",
    "    return jsonify(station_list)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "    session = Session(engine)\n",
    "    start_date = dt.date(2016,8,23)\n",
    "    results = session.query(measurement.date, measurement.tobs).filter(measurement.date > start_date).filter(Measurement.station == 'USC00519281').all()\n",
    "    session.close()\n",
    "\n",
    "    temp_tobs = []\n",
    "    for date, temp in results:\n",
    "        dict = {}\n",
    "        dict[\"Date\"] = date\n",
    "        dict[\"Temperature\"] = temp\n",
    "        tobs.append(dict)\n",
    "\n",
    "    return jsonify(temp_tobs)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/<start>\")\n",
    "def start():\n",
    "    start_date = dt.date(2016,8,23)\n",
    "    end_date = dt.date(2017,8,23)\n",
    "    session = Session(engine)\n",
    "    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(Measurement.date >= start_date).all()\n",
    "    session.close()\n",
    "\n",
    "    temp_summ = []\n",
    "    for min, avg, max in results:\n",
    "        dict = {}\n",
    "        dict[\"Minimum Temperature\"] = min\n",
    "        dict[\"Avgerage Temperature\"] = avg\n",
    "        dict[\"Maximum Temperature\"] = max\n",
    "        temp_summ.append(dict)\n",
    "        \n",
    "    return jsonify(temp_summ)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [17/Jul/2020 17:18:26] \"\u001b[37mGET / HTTP/1.1\u001b[0m\" 200 -\n",
      "127.0.0.1 - - [17/Jul/2020 17:18:26] \"\u001b[33mGET /favicon.ico HTTP/1.1\u001b[0m\" 404 -\n",
      "127.0.0.1 - - [17/Jul/2020 17:18:40] \"\u001b[33mGET /tobs HTTP/1.1\u001b[0m\" 404 -\n",
      "127.0.0.1 - - [17/Jul/2020 17:20:23] \"\u001b[37mGET / HTTP/1.1\u001b[0m\" 200 -\n"
     ]
    }
   ],
   "source": [
    "@app.route(\"/api/v1.0/<start_date>/<end_date>\")\n",
    "def start_end():\n",
    "    session = Session(engine)\n",
    "    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date > start_date).filter(measurement.date < end_date).all()\n",
    "    session.close()\n",
    "\n",
    "    temp_summ2 = []\n",
    "    for min, avg, max in results:\n",
    "        dict = {}\n",
    "        dict[\"Minimum Temperature\"] = min\n",
    "        dict[\"Avgerage Temperature\"] = avg\n",
    "        dict[\"Maximum Temperature\"] = max\n",
    "        temp_summ.append(dict)\n",
    "        \n",
    "    return jsonify(temp_summ2)\n",
    "        \n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=False)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
