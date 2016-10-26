package id.artificialintelligence.rojak.models;

public class PairOfCandidates {
    private int id;
    private String name;
    private String websiteUrl;
    private String logoUrl;
    private String fbpageUsername;
    private String twitterUsername;
    private String instagramUsername;
    private String slogan;
    private String description;
    private int cagubId;
    private int cawagubId;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getWebsiteUrl() {
        return websiteUrl;
    }

    public void setWebsiteUrl(String websiteUrl) {
        this.websiteUrl = websiteUrl;
    }

    public String getLogoUrl() {
        return logoUrl;
    }

    public void setLogoUrl(String logoUrl) {
        this.logoUrl = logoUrl;
    }

    public String getFbpageUsername() {
        return fbpageUsername;
    }

    public void setFbpageUsername(String fbpageUsername) {
        this.fbpageUsername = fbpageUsername;
    }

    public String getTwitterUsername() {
        return twitterUsername;
    }

    public void setTwitterUsername(String twitterUsername) {
        this.twitterUsername = twitterUsername;
    }

    public String getInstagramUsername() {
        return instagramUsername;
    }

    public void setInstagramUsername(String instagramUsername) {
        this.instagramUsername = instagramUsername;
    }

    public String getSlogan() {
        return slogan;
    }

    public void setSlogan(String slogan) {
        this.slogan = slogan;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public int getCagubId() {
        return cagubId;
    }

    public void setCagubId(int cagubId) {
        this.cagubId = cagubId;
    }

    public int getCawagubId() {
        return cawagubId;
    }

    public void setCawagubId(int cawagubId) {
        this.cawagubId = cawagubId;
    }
}
