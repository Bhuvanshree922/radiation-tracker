FROM flink:1.17.2-scala_2.12-java11
COPY target/radiation.jar /opt/flink/usrlib/radiation.jar
