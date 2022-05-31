package main

import (
	"github.com/gin-gonic/gin"
	"os"
	"strings"
)

func admin(c *gin.Context) {
	staticPath := "/app/static/crt/"
	oldname := c.DefaultQuery("oldname", "")
	newname := c.DefaultQuery("newname", "")
	if oldname == "" || newname == "" || strings.Contains(oldname, "..") || strings.Contains(newname, "..") {
		c.String(500, "error")
		return
	}
	if c.Request.URL.RawPath != "" && c.Request.Host == "admin" {
		err := os.Rename(staticPath+oldname, staticPath+newname)
		if err != nil {
			return
		}
		c.String(200, newname)
		return
	}
	c.String(200, "no")
}

func index(c *gin.Context) {
	c.String(200, "hello world")
}

func main() {
	router := gin.Default()
	router.GET("/", index)
	router.GET("/admin/rename", admin)

	if err := router.Run(":8887"); err != nil {
		panic(err)
	}
}
