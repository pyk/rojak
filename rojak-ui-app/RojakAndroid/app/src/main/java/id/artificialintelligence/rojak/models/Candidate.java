package id.artificialintelligence.rojak.models;


import com.google.gson.annotations.SerializedName;

public class Candidate {
    @SerializedName("id") private int id;
    @SerializedName("full_name") private String fullName;
    @SerializedName("alias_name") private String aliasName;
    @SerializedName("place_of_birth") private String placeOfBirth;
    @SerializedName("date_of_birth") private String dateOfBirth;
    @SerializedName("religion") private String religion;
    @SerializedName("website_url") private String websiteUrl;
    @SerializedName("photo_url") private String photoUrl;
    @SerializedName("fbpage_username") private String fbpageUsername;
    @SerializedName("twitter_username") private String twitterUsername;
    @SerializedName("instagram_username") private String instagramUsername;

    public String getAliasName() {
        return aliasName;
    }

    public void setAliasName(String aliasName) {
        this.aliasName = aliasName;
    }

    public String getDateOfBirth() {
        return dateOfBirth;
    }

    public void setDateOfBirth(String dateOfBirth) {
        this.dateOfBirth = dateOfBirth;
    }

    public String getFbpageUsername() {
        return fbpageUsername;
    }

    public void setFbpageUsername(String fbpageUsername) {
        this.fbpageUsername = fbpageUsername;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
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

    public String getPhotoUrl() {
        return photoUrl;
    }

    public void setPhotoUrl(String photoUrl) {
        this.photoUrl = photoUrl;
    }

    public String getPlaceOfBirth() {
        return placeOfBirth;
    }

    public void setPlaceOfBirth(String placeOfBirth) {
        this.placeOfBirth = placeOfBirth;
    }

    public String getReligion() {
        return religion;
    }

    public void setReligion(String religion) {
        this.religion = religion;
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
