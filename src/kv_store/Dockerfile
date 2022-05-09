FROM alpine:3.15
RUN apk add python3 py3-pip make
WORKDIR /app
COPY . .
RUN make install
ENTRYPOINT [ "make" ]
CMD ["run"]
EXPOSE 8080
