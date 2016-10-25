package id.artificialintelligence.rojak.models;


public class Media {
    private int id;
    private String name;
    private String websiteUrl;
    private String logoUrl;
    private String fbPageUsername;
    private String twitterUsername;
    private String instagramUsername;

    public String getFbPageUsername() {
        return fbPageUsername;
    }

    public void setFbPageUsername(String fbPageUsername) {
        this.fbPageUsername = fbPageUsername;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getInstagramUsername() {
        return instagramUsername;
    }

    public void setInstagramUsername(String instagramUsername) {
        this.instagramUsername = instagramUsername;
    }

    public String getLogoUrl() {
        return logoUrl;
    }

    public void setLogoUrl(String logoUrl) {
        this.logoUrl = logoUrl;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getTwitterUsername() {
        return twitterUsername;
    }

    public void setTwitterUsername(String twitterUsername) {
        this.twitterUsername = twitterUsername;
    }

    public String getWebsiteUrl() {
        return websiteUrl;
    }

    public void setWebsiteUrl(String websiteUrl) {
        this.websiteUrl = websiteUrl;
    }
}
