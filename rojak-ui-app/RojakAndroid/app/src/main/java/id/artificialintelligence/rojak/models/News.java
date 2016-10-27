package id.artificialintelligence.rojak.models;


import com.google.gson.annotations.SerializedName;

public class News {
    @SerializedName("id") private int id;
    @SerializedName("media_id") private int mediaId;
    @SerializedName("title") private String title;
    @SerializedName("url") private String url;
    @SerializedName("author_name") private String authorName;

    public String getAuthorName() {
        return authorName;
    }

    public void setAuthorName(String authorName) {
        this.authorName = authorName;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getMediaId() {
        return mediaId;
    }

    public void setMediaId(int mediaId) {
        this.mediaId = mediaId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }
}
