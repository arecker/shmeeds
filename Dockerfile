FROM golang:1.18-alpine as build
WORKDIR /app
COPY go.mod ./
COPY go.sum ./
RUN go mod download
COPY *.go ./
RUN CGO_ENABLED=0 go build -o /shmeeds

FROM gcr.io/distroless/base-debian10
WORKDIR /
COPY --from="build" /shmeeds /shmeeds
USER nonroot:nonroot
ENTRYPOINT ["/shmeeds"]
