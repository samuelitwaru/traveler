from flask_restful import reqparse, inputs

get_buses_parser = reqparse.RequestParser()
get_buses_parser.add_argument('departure_time', type=inputs.datetime_from_iso8601, help='Invalid depature_date', location="args")
get_buses_parser.add_argument('company_id', type=int, help='Invalid company_id', location="args")
get_buses_parser.add_argument('from', type=str, help='Invalid from', location="args")
get_buses_parser.add_argument('to', type=str, help='Invalid to', location="args")