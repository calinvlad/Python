from flask import Flask, request, jsonify


def get():
    return jsonify({'msg': 'Home'})
