from flask import Flask, request, jsonify
from backend.core import predict
from backend.config import DEBUG_MODE

app = Flask(__name__)